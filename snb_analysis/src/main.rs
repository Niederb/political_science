use walkdir::WalkDir;

use plotly::common::Title;
use plotly::layout::{Axis, Layout};
use plotly::{Bar, Plot};

use std::env;

fn get_report_lengths(path: &str) -> (Vec<String>, Vec<usize>) {
    let walker = WalkDir::new(path).into_iter();

    let mut years = Vec::new();
    let mut report_lengths = Vec::new();

    for entry in walker.filter_map(|e| e.ok()) {
        let path = entry.into_path();
        if let Some(os_ext) = path.extension() {
            if let Some(ext) = os_ext.to_str() {
                if ext == "pdf" {
                    let d = lopdf::Document::load(&path).unwrap();
                    let number_of_pages = d.get_pages().len();
                    let year_string = path.parent().unwrap().file_stem().unwrap();
                    let year_string = year_string.to_str().unwrap().to_owned();
                    println!("{:?};{}", &year_string, &number_of_pages);

                    years.push(year_string);
                    report_lengths.push(number_of_pages);
                }
            }
        }
    }
    (years, report_lengths)
}

fn create_plot(years: Vec<String>, report_lengths: Vec<usize>) {
    let trace = Bar::new(years, report_lengths).name("report_lengths");
    let layout = Layout::new()
        .title(Title::new("Swiss National Bank Annual Report Length"))
        .x_axis(Axis::new().title(Title::new("Year")))
        .y_axis(Axis::new().title(Title::new("Pages")));
    let mut plot = Plot::new();
    plot.set_layout(layout);
    plot.add_trace(trace);
    plot.show();
}

fn main() {
    let args: Vec<String> = env::args().collect();

    if args.len() != 1 {
        println!("Usage: snp_analysis <directory_with_reports>");
    } else {
        let path = &args[0];
        let (years, report_lengths) = get_report_lengths(&path);
        create_plot(years, report_lengths);
    }
}
