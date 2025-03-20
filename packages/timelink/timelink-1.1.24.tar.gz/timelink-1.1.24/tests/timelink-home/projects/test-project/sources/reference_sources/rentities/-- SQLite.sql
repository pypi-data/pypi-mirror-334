-- SQLite
-- SQLite
SELECT r.id, r.origin, r.destination, r.the_type, r.the_value
FROM relations r, entities e
WHERE r.id = e.id
    AND e.the_source != 'sameas-tests'
    AND r.destination IN
    (SELECT id FROM entities e2
      WHERE e2.id = r.destination
      AND e2.the_source != e.the_source)
;
-- Path: tests/--%20SQLite.sql
-- SQLite
SELECT l.rid,l.entity,l.source as link_source, e.the_source as entity_source from links l, entities e
WHERE l.entity = e.id AND
   entity_source = 'sameas-tests' AND
   link_source != entity_source;
--
SELECT * FROM relations WHERE destinatio ISNULL;