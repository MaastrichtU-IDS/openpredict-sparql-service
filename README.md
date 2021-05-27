# SPARQL endpoint for OpenPredict

A SPARQL endpoint to serve predictions generated using the OpenPredict classifier.

## Example queries 📬

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
  SERVICE <https://sparql-openpredict.137.120.31.102.nip.io/sparql> {
	SELECT ?drugOrDisease ?predictedForTreatment WHERE {
    	BIND("OMIM:246300" AS ?drugOrDisease)
    	BIND(openpredict:prediction(?drugOrDisease) AS ?predictedForTreatment)
	}
  }
}q
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

