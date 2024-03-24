
link: https://dbpedia.org/sparql/
## Qury en

DIseases in en: 16643

```
PREFIX dbo: <http://dbpedia.org/ontology/>
SELECT (COUNT(?disease) AS ?count)
WHERE {
  ?disease rdf:type dbo:Disease ;
           rdfs:label ?diseaseLabel ;
           dbo:abstract ?abstract .
  FILTER(LANG(?diseaseLabel) = 'en' && LANG(?abstract) = 'en')
}

```
## Query es 
Disease in es : 136183


```
PREFIX dbo: <http://dbpedia.org/ontology/>
SELECT (COUNT(?disease) AS ?count)
WHERE {
  ?disease rdf:type dbo:Disease ;
           rdfs:label ?diseaseLabel ;
           dbo:abstract ?abstract .
  FILTER(LANG(?diseaseLabel) = 'es' && LANG(?abstract) = 'es')
}

```