use walkdir::WalkDir;

use plotly::common::{
    ColorScale, ColorScalePalette, DashType, Fill, Font, Line, LineShape, Marker, Mode, Title,
};
use plotly::layout::{Axis, BarMode, Layout, Legend, TicksDirection};
use plotly::{Bar, NamedColor, Plot, Rgb, Rgba, Scatter};

fn main() {
    let path = r"D:\Repository\annual_report_database\downloads\2021-01-08\Schweizerische Nationalbank";
    let walker = WalkDir::new(path).into_iter();

    let mut years = Vec::new();
    let mut report_lengths = Vec::new();

    for entry in walker.filter_map(|e| e.ok()) {
        let path = entry.into_path();
        if let Some(os_ext) = path.extension() {
            if let Some(ext) = os_ext.to_str() {
                if ext == "pdf" {
                    let d = lopdf::Document::load(&path).unwrap();
                    let page_number = d.get_pages().len();
                    let year_string = path.parent().unwrap().file_stem().unwrap();
                    let year_string = year_string.to_str().unwrap().to_owned();
                    println!("{:?};{}", &year_string, &page_number);

                    years.push(year_string);
                    report_lengths.push(page_number);
                }
            }
        }
    }
    let trace = Scatter::new(years, report_lengths)
        .mode(Mode::LinesMarkers)
        .line(Line::new().width(7.0))
        .name("Scatter");
    // https://www.snb.ch/de/iabout/pub/id/pub_annrep
    let layout = Layout::new().title(Title::new("Swiss National Bank Annual Report Length"))
        .x_axis(Axis::new().title(Title::new("Year")))
        .y_axis(Axis::new().title(Title::new("Pages")));
    let mut plot = Plot::new();
    plot.set_layout(layout);
    plot.add_trace(trace);
    plot.show();
}
