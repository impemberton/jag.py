# jag.py
Just Another Generator

This is an attempt to create a static site generator for my blog at [impemberton.com](https://www.impemberton.com)

## RoadMap

**End Goal**: Generate a complete static site with the below folder hierarchy

```
--site
  |--index.html
  |
  |--about
  |  |--index.html
  |
  |--contact
  |  |--index.html
  |
  |--articles
  |  |--article1
  |  |  |--index.html
  |  |  
  |  |--article2
  |  |  |--index.html
  |  |
  |  |-- ...
  | 
  |--tags
     |--tag_1
     |  |--index.html
     |--tag_2
     |  |--index.html
     |
     |-- ...
```

We want each folder to contain its own index.html for the URLs to look clean.


**Current Goal**: Convert a single markdown file into an html article.

My website's HTML files currently uses the following basic structure:

```
  <head></head> <!-- everything in head remains the same except the title -->
  <body>
    <nav></nav> <!-- nav is the same on every page -->
    <article>
     Here is where my markdown will be converted into HTML!
    </article>
  </body>
</html>
```

So I simply need to convert markdown into the appropriate HTML Tags. Here we go...
