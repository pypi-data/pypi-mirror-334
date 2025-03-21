use super::sheet::{CellData, SheetWriter};
use pyo3::prelude::*;
use quick_xml::events::{BytesDecl, BytesEnd, BytesStart, Event};
use quick_xml::Writer;
use std::io::Write;
use zip::write::SimpleFileOptions;
use zip::{CompressionMethod, ZipWriter};

#[pyclass]
pub struct BookWriter {
    sheet_writers: Vec<SheetWriter>,
    zip_writer: ZipWriter<std::fs::File>,
}

#[pymethods]
impl BookWriter {
    #[new]
    fn new(name: &str) -> Self {
        let file = std::fs::File::create(name).expect(&format!("create file {name} error!"));
        BookWriter {
            sheet_writers: Vec::new(),
            zip_writer: ZipWriter::new(file),
        }
    }

    fn add_sheet(&mut self, name: &str, headers: Vec<String>) {
        let sheet_writer = SheetWriter::new(name, headers);
        self.sheet_writers.push(sheet_writer);
    }

    fn add_column_str(&mut self, sheet_idx: usize, series: Vec<String>) {
        let cell_series: Vec<CellData> = series.into_iter().map(CellData::String).collect();
        self.add_column(sheet_idx, cell_series);
    }

    fn add_column_number(&mut self, sheet_idx: usize, series: Vec<f64>) {
        let cell_series: Vec<CellData> = series.into_iter().map(CellData::Number).collect();
        self.add_column(sheet_idx, cell_series);
    }

    fn save(&mut self) {
        self.write_content_types().expect("fail to write: [Content_Types].xml");
        self.write_root_rels().expect("fail to write: _rels/.rels");
        self.write_workbook().expect("failed to write: xl/workbook.xml");
        self.write_styles().expect("failed to write: xl/styles.xml");
        self.write_workbook_rels().expect("failed to write: xl/_rels/workbook.xml.rels");
        self.write_sheets().expect("failed to write: xl/worksheets/sheet*.xml");
        let unsafe_zip_writer = unsafe { std::ptr::read(&mut self.zip_writer) }; // in order must use `&must self` for pyo3
        unsafe_zip_writer.finish().expect("failed to save file");
    }
}

impl BookWriter {
    fn add_column(&mut self, sheet_idx: usize, series: Vec<CellData>) {
        if let Some(sheet_writer) = self.sheet_writers.get_mut(sheet_idx) {
            sheet_writer.add_column(series);
        } else {
            println!("add column failed, sheet_idx should in [0, {}]", self.sheet_writers.len());
        }
    }

    fn write_styles(&mut self) -> Result<(), std::io::Error> {
        let mut writer = Writer::new(Vec::new());
        writer.write_event(Event::Decl(BytesDecl::new("1.0", Some("UTF-8"), Some("yes"))))?;

        let mut root = BytesStart::new("styleSheet");
        root.push_attribute(("xmlns", "http://schemas.openxmlformats.org/spreadsheetml/2006/main"));
        writer.write_event(Event::Start(root))?;
        writer.write_event(Event::End(BytesEnd::new("styleSheet")))?;

        // write styles
        self.zip_writer.start_file(
            "xl/styles.xml",
            SimpleFileOptions::default().compression_method(CompressionMethod::Deflated),
        )?;
        self.zip_writer.write_all(&writer.into_inner())?;
        Ok(())
    }

    fn write_root_rels(&mut self) -> Result<(), std::io::Error> {
        let mut writer = Writer::new(Vec::new());
        writer.write_event(Event::Decl(BytesDecl::new("1.0", Some("UTF-8"), Some("yes"))))?;

        let mut root = BytesStart::new("Relationships");
        root.push_attribute(("xmlns", "http://schemas.openxmlformats.org/package/2006/relationships"));
        writer.write_event(Event::Start(root))?;
        writer.write_event(Event::Empty(BytesStart::new("Relationship").with_attributes(vec![
            ("Id", "rId1"),
            (
                "Type",
                "http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument",
            ),
            ("Target", "xl/workbook.xml"),
        ])))?;

        writer.write_event(Event::End(BytesEnd::new("Relationships")))?;

        // write relationships
        self.zip_writer.start_file(
            "_rels/.rels",
            SimpleFileOptions::default().compression_method(CompressionMethod::Deflated),
        )?;
        self.zip_writer.write_all(&writer.into_inner())?;
        Ok(())
    }

    fn write_content_types(&mut self) -> Result<(), std::io::Error> {
        let mut writer = Writer::new(Vec::new());
        writer.write_event(Event::Decl(BytesDecl::new("1.0", Some("UTF-8"), Some("yes"))))?;

        let mut root = BytesStart::new("Types");
        root.push_attribute(("xmlns", "http://schemas.openxmlformats.org/package/2006/content-types"));
        writer.write_event(Event::Start(root))?;

        // Defaults
        writer.write_event(Event::Empty(BytesStart::new("Default").with_attributes(vec![
            ("Extension", "rels"),
            ("ContentType", "application/vnd.openxmlformats-package.relationships+xml"),
        ])))?;

        // Workbook
        writer.write_event(Event::Empty(BytesStart::new("Override").with_attributes(vec![
            ("PartName", "/xl/workbook.xml"),
            (
                "ContentType",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml",
            ),
        ])))?;

        // Worksheets (use index-based filenames)
        for (idx, _) in self.sheet_writers.iter().enumerate() {
            writer.write_event(Event::Empty(BytesStart::new("Override").with_attributes(vec![
                ("PartName", format!("/xl/worksheets/sheet{}.xml", idx + 1).as_str()),
                ("ContentType", "application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"),
            ])))?;
        }

        writer.write_event(Event::End(BytesEnd::new("Types")))?;

        // write workbook.xml
        self.zip_writer.start_file(
            "[Content_Types].xml",
            SimpleFileOptions::default().compression_method(CompressionMethod::Deflated),
        )?;
        self.zip_writer.write_all(&writer.into_inner())?;
        Ok(())
    }

    fn write_workbook_rels(&mut self) -> Result<(), std::io::Error> {
        let mut writer = Writer::new(Vec::new());
        writer.write_event(Event::Decl(BytesDecl::new("1.0", Some("UTF-8"), Some("yes"))))?;

        let mut root = BytesStart::new("Relationships");
        root.push_attribute(("xmlns", "http://schemas.openxmlformats.org/package/2006/relationships"));
        writer.write_event(Event::Start(root))?;

        // Worksheet relationships (use index-based filenames)
        for (idx, _) in self.sheet_writers.iter().enumerate() {
            writer.write_event(Event::Empty(BytesStart::new("Relationship").with_attributes(vec![
                ("Id", format!("rId{}", idx + 1).as_str()),
                ("Type", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet"),
                ("Target", &format!("worksheets/sheet{}.xml", idx + 1)),
            ])))?;
        }

        writer.write_event(Event::End(BytesEnd::new("Relationships")))?;

        // write workbook.xml.rels
        self.zip_writer.start_file(
            "xl/_rels/workbook.xml.rels",
            SimpleFileOptions::default().compression_method(CompressionMethod::Deflated),
        )?;
        self.zip_writer.write_all(&writer.into_inner())?;
        Ok(())
    }

    fn write_workbook(&mut self) -> Result<(), std::io::Error> {
        let mut writer = Writer::new(Vec::new());
        writer.write_event(Event::Decl(BytesDecl::new("1.0", Some("UTF-8"), Some("yes"))))?;

        let mut root = BytesStart::new("workbook");
        root.push_attribute(("xmlns", "http://schemas.openxmlformats.org/spreadsheetml/2006/main"));
        root.push_attribute(("xmlns:r", "http://schemas.openxmlformats.org/officeDocument/2006/relationships"));
        writer.write_event(Event::Start(root))?;

        writer.write_event(Event::Start(BytesStart::new("sheets")))?;

        // Generate sheets in insertion order with correct rIds
        for (idx, sheet_writer) in self.sheet_writers.iter().enumerate() {
            let mut sheet = BytesStart::new("sheet");
            sheet.push_attribute(("name", sheet_writer.name.as_str()));
            sheet.push_attribute(("sheetId", (idx + 1).to_string().as_str()));
            sheet.push_attribute(("r:id", format!("rId{}", idx + 1).as_str()));
            writer.write_event(Event::Empty(sheet))?;
        }

        writer.write_event(Event::End(BytesEnd::new("sheets")))?;
        writer.write_event(Event::End(BytesEnd::new("workbook")))?;

        // write workbook.xml
        self.zip_writer.start_file(
            "xl/workbook.xml",
            SimpleFileOptions::default().compression_method(CompressionMethod::Deflated),
        )?;
        self.zip_writer.write_all(&writer.into_inner())?;
        Ok(())
    }

    fn write_sheets(&mut self) -> Result<(), std::io::Error> {
        for (sheet_idx, sheet_writer) in self.sheet_writers.iter().enumerate() {
            self.zip_writer.start_file(
                &format!("xl/worksheets/sheet{}.xml", sheet_idx + 1),
                SimpleFileOptions::default().compression_method(CompressionMethod::Deflated),
            )?;
            self.zip_writer.write_all(&sheet_writer.generate_xml()?)?;
        }
        Ok(())
    }
}
