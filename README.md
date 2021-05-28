# SPARQL endpoint for OpenPredict

A SPARQL endpoint to serve predictions generated using the OpenPredict classifier, using custom SPARQL functions. Built with [rdflib-endpoint](https://github.com/vemonet/rdflib-endpoint)

Access the SPARQL service endpoint at https://service.openpredict.137.120.31.102.nip.io/sparql

OpenAPI docs at https://service.openpredict.137.120.31.102.nip.io


## Available functions 🧪

**<a href="https://yasgui.triply.cc/#query=PREFIX%20openpredict%3A%20%3Chttps%3A%2F%2Fw3id.org%2Fum%2Fopenpredict%2F%3E%0ASELECT%20%3FdrugOrDisease%20%3FpredictedForTreatment%20%3FpredictedForTreatmentScore%20WHERE%20%7B%0A%20%20%20%20BIND(%22OMIM%3A246300%22%20AS%20%3FdrugOrDisease)%0A%20%20%20%20BIND(openpredict%3Aprediction(%3FdrugOrDisease)%20AS%20%3FpredictedForTreatment)&endpoint=https%3A%2F%2Fservice.openpredict.137.120.31.102.nip.io%2Fsparql&requestMethod=GET&tabTitle=Query%209&headers=%7B%7D&contentTypeConstruct=application%2Fn-triples%2C*%2F*%3Bq%3D0.9&contentTypeSelect=application%2Fsparql-results%2Bjson%2C*%2F*%3Bq%3D0.9&outputFormat=table">Try the queries on YASGUI</a>**

### Get predictions

Query OpenPredict classifier to get drug/disease predictions

```SPARQL
PREFIX openpredict: <https://w3id.org/um/openpredict/>
SELECT ?drugOrDisease ?predictedForTreatment ?predictedForTreatmentScore WHERE {
    BIND("OMIM:246300" AS ?drugOrDisease)
    BIND(openpredict:prediction(?drugOrDisease) AS ?predictedForTreatment)
```

### Try a federated query

Use this federated query to retrieve predicted treatments for a drug or disease (OMIM or DRUGBANK) from any other SPARQL endpoint supporting federated queries.

```SPARQL
PREFIX openpredict: <https://w3id.org/um/openpredict/>
SELECT * WHERE
{
  SERVICE <https://service.openpredict.137.120.31.102.nip.io/sparql> {
	SELECT ?drugOrDisease ?predictedForTreatment WHERE {
    	BIND("OMIM:246300" AS ?drugOrDisease)
    	BIND(openpredict:prediction(?drugOrDisease) AS ?predictedForTreatment)
	}
  }
}
```

## Install and run ✨️

1. Install dependencies

```bash
pip install -r requirements.txt
```

2. Run the server on http://localhost:8000

```bash
uvicorn main:app --reload --app-dir app
```

## Or run with docker 🐳

Checkout the `Dockerfile` to see how the image is built, and run it with the `docker-compose.yml`:

```bash
docker-compose up -d --build
```

