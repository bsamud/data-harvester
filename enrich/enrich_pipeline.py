class EnrichmentPipeline:
    def __init__(self):
        self.enrichers = []

    def add_enricher(self, enricher):
        self.enrichers.append(enricher)

    def enrich(self, data):
        for enricher in self.enrichers:
            data = enricher.process(data)
        return data
