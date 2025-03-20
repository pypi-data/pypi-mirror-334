# ChartArt Package is under development

Use 
[Github-flavored Markdown](https://guides.github.com/features/mastering-markdown/)
to write your content.

Change Log 

0.0.1 => 0.0.2 
Added support for =>
-Publish post without javascript package from notebook
-Pulish post from standalone python script (Non jupyter environment)


0.0.2 => 0.0.3 
Added support for features at the time of publishing post. Features will get used as filters.

0.0.3.dev5 => 0.0.3.dev6
-Support for status posts compatible with new low code platform.
Example: 

```

filters = {
    "dateAdded": datetime.datetime.now().isoformat() + 'Z',
    'rowSubscriptionCol': 'vendor',
    'type': 'aggregatePost'
}

data = {
    'count': 5,
    'status': 'Warning',
    'vendor': 'GCP'
}

post = Post(postId='GCP_aggregatePost', postTitle='# Aggregated Post')
post.addFilters(filters)
post.createPost(data=data)

```
0.0.3.dev6 => 0.0.3.dev7
-Added Exception handling code if response is not in json format

0.0.3.dev7 => 0.0.3.dev8
-Added code to retry 5xx error code 

0.0.3.dev7 => 0.0.3.dev10
-Resolved unauthorized error and changed sleep time

0.0.3.dev12 => 0.0.3.dev13
- Added line/bar/scatter chart subtypes
- line type : line, area, spline, stepLine, splineArea, stepArea, stackedLine, stackedArea, stackedArea100, stackedLine100
- bar type : bar,column,stackedBar,stackedColumn,stackedBar,stackedBar100,stackedColumn100  
- scatter : bubble , if size is specified as list of float scatter chart will get ploted as bubble chart

0.0.3.dev14 => 0.0.3.dev15
- Tree Map : c (color) param is optional
- Map : shapeDataField is new optional param (defaults to key 'Name'). primaryValueMapper and data is optional parameters now. This will be usefull for markers/bubbles where we dont need these inputs.
- Map : added support fo sub layers. 

0.0.3.dev18
- Added startAngle, endAngle, radius, groupTo in circular chart
- Added number format on axis

0.0.3.dev19
- added support to specify axis type 
- Made default bin interval is 0 . 0 means syncfusion will calculate internally.

0.0.3.dev20
- preview and previewPost url should route should start with /  e.g  earlier http://localhost:port/#preview  now http://localhost:port/#/preview

0.0.3.dev21
- Fix for communicate with Jupyter kernel

0.0.3.dev22
- Fix for setting axis type on figure object

0.0.3.dev23
- Added tooltip related parameters for map

0.0.3.dev25
- Added datetime.date as supported type for datetime axis

0.0.3.dev26
- Inmemory chart inside post

0.0.3.dev29
- Inmemory aggregate posts

0.0.3.dev30
- for table chart now we can specify column types.
- by default we will not show index column in table. User can specify it if needed.

0.0.3.dev31
- Resolved issue of technical indicator in charts

0.0.3.dev32
- Moved candle chart under cartesian chart ubrella
- Added generic method to add charts mainly required for drilldown table

0.0.3.dev33
- Multi axis support

0.0.3.dev34
- Date time axis x support for bar chart. Removed check of check_not_datetime(x)

0.0.3.dev35
- support for isVisibleInLegend on series

0.0.3.dev36
- support for drilldown details at figure level.

0.0.3.dev37
- Handling categorical value for line and bar

0.0.3.dev38
- Handling categorical value for line and bar

0.0.3.dev39
- Handling categorical value for line and bar

0.0.3.dev40
- support for pdf export

0.0.3.dev41
- Fix for for pdf export

0.0.3.dev42
- Fix for for pdf export
