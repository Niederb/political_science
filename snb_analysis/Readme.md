# Data analysis with Rust

## Data

## Libraries

For this small analysis I decided to just use a pdf library and a plotting library. The actual data analysis part is basically non-existent, so I decided against using a data analysis library.

## Processing

### Getting report lengths

For this we need to get the page lengths from all the pdfs. Luckly there are multiple pdf crates available. I decided to go with the [lopdf](https://crates.io/crates/lopdf) crate.

Luckily the plotly crate makes it quite easy to load a document and get the number of pages out of it:

```rust
let d = lopdf::Document::load(&path).unwrap();
let number_of_pages = d.get_pages().len();
```

So we just iterate over all the files and get the information we need out of them. Afterwards we just create two vectors: One with the year, which we extract from the folder name, and one with the extracted page numbers.

### Creating the plot

For plotting I decided to go with the [plotly](https://crates.io/crates/plotly) crate which provides an API to [plotly](https://plotly.com/javascript/). We just pass in out two vectors (`year` and `number_of_pages`) into `Bar::new(..)`, add a title and names for the axis:

```rust
    let trace = Bar::new(years, report_lengths)
        .name("report_lengths");
    let layout = Layout::new()
        .title(Title::new("Swiss National Bank Annual Report Length"))
        .x_axis(Axis::new().title(Title::new("Year")))
        .y_axis(Axis::new().title(Title::new("Pages")));
    let mut plot = Plot::new();
    plot.set_layout(layout);
    plot.add_trace(trace);
    plot.show();
```

## Conclusion

Overall I was easier than expected to create this simple analysis. Finding and selecting the libraries that I neede took probably most of the time.

One thing that I really like with Rust is, how many errors the compiler can find. Especially with hobby projects, on which I only work every couple of weeks.
