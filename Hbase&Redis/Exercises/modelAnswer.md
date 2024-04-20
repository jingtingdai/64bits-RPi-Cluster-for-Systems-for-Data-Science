
## Model Answer 6

1. & 2. As the exercises were about applying the steps described in tutorials, there are no model answers as such. Applying the steps is pretty straightforward. However, should there be questions about parts of the tutorials, please also post these questions into the forum even when asking during the exercise. In this way, everyone can see the answer.


3.  c) i.
- `scan 'wiki_small', {STARTROW=>'100009', ENDROW=>'100011'}` returns the five keys 1000092, 1000102, 1000104, 1000106, 1000108,

- `scan 'wiki_small', {STARTROW=>'100015', ENDROW=>'100016'}` returns the seven keys 100015, 1000151, 1000153, 1000155, 1000156, 1000158, 1000159.

  Rows are sorted lexicographically (not numerically) by row key, in our case by `page_id`. In order to get numerical order, the keys would have to be padded, otherwise e.g. 10 is lexicographically smaller than 2.

  - 
    - A. `scan 'wiki_small', {COLUMNS => ['page:page_title', 'author:contributor_name'], ROWPREFIXFILTER => '1977'}`

    - B. `scan 'wiki_small', {COLUMNS => ['page:page_title', 'author:contributor_name'], FILTER => "SingleColumnValueFilter('author', 'contributor_name', =, 'substring:tom')"}`
  
  - 
    - A. For a quick test, let us return the first five results:
      ```
      scan 'wiki_small', {COLUMNS => 'author:timestamp', FILTER => "ValueFilter(=, 'substring:2017')", LIMIT=>5}
      ```
      
      Next, we fetch all the results:
      ```
      scan 'wiki_small', {COLUMNS => 'author:timestamp', FILTER => "ValueFilter(=, 'substring:2017')"}
      ```
      
    - B. `scan 'wiki_small', {COLUMNS => 'page:page_title', FILTER => "ValueFilter(=, 'substring:Sydney')"}`
      
      which returns 280 rows. Another formulation of the query is
      ```
      scan 'wiki_small', {FILTER => "SingleColumnValueFilter('page', 'page_title', =, 'substring:Sydney')"}
      ```
