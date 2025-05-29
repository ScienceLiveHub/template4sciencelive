# Create Nanopublication Templates For sciencelive

The idea would be to enable users to create new templates by combining existing ones. For instance, we could combine the AIDA nanopublication template with a location template and a temporal coverage template to create a new template that includes all three.

As a first step, we are exploring how to create new nanopublication templates.

## Template with spatio-temporal coverage

```
Python scripts to help generating nanopublication templates for the Science Live Project. 
@prefix this: <https://w3id.org/np/RASpatio-TemporalAIDA-Template123> .
@prefix sub: <https://w3id.org/np/RASpatio-TemporalAIDA-Template123#> .
@prefix np: <http://www.nanopub.org/nschema#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix nt: <https://w3id.org/np/o/ntemplate/> .
@prefix npx: <http://purl.org/nanopub/x/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix orcid: <https://orcid.org/> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix schema: <http://schema.org/> .
@prefix geo: <http://www.opengis.net/ont/geosparql#> .

sub:Head {
  this: np:hasAssertion sub:assertion;
    np:hasProvenance sub:provenance;
    np:hasPublicationInfo sub:pubinfo;
    a np:Nanopublication .
}

sub:assertion {
  # Define labels for properties
  <http://purl.org/petapico/o/hycl#AIDA-Sentence> rdfs:label "AIDA sentence - Atomic, Independent, Declarative, and Absolute" .
  
  <http://purl.org/spar/cito/obtainsSupportFrom> rdfs:label "is supported by" .
  
  schema:about rdfs:label "is about - connects a thing (left) to a subject matter that this thing is about (right)" .
  
  rdf:type rdfs:label "is an - connects a thing (left) to a class it belongs to (right)" .
  
  <http://www.w3.org/2004/02/skos/core#related> rdfs:label "is related to" .
  
  dct:spatial rdfs:label "has spatial coverage" .
  
  dct:temporal rdfs:label "has temporal extent" .
  
  dcat:spatialResolutionInMeters rdfs:label "has spatial resolution in meters" .
  
  dcat:temporalResolution rdfs:label "has temporal resolution" .
  
  # Define the AIDA sentence placeholder
  sub:aida a nt:AutoEscapeUriPlaceholder, nt:IntroducedResource;
    rdfs:label "Type your AIDA sentence here (ending with a full stop)";
    nt:hasPrefix "http://purl.org/aida/";
    nt:hasPrefixLabel "The sentence";
    nt:hasRegex "[\\S ]{5,500}\\." .
  
  # Define spatial coverage placeholders
  sub:spatialCoverage a nt:LiteralPlaceholder;
    rdfs:label "Spatial coverage (e.g., WKT geometry, place name, or bounding box)";
    nt:hasRegex ".{2,500}" .
  
  sub:spatialResolution a nt:LiteralPlaceholder;
    rdfs:label "Spatial resolution in meters (optional)";
    nt:hasDatatype xsd:decimal .
  
  # Define temporal coverage placeholders
  sub:temporalStart a nt:LiteralPlaceholder;
    rdfs:label "Temporal coverage start (ISO 8601 format, e.g., 2023-01-01 or 2023-01-01T00:00:00Z)";
    nt:hasDatatype xsd:dateTime .
  
  sub:temporalEnd a nt:LiteralPlaceholder;
    rdfs:label "Temporal coverage end (ISO 8601 format, e.g., 2023-12-31 or 2023-12-31T23:59:59Z)";
    nt:hasDatatype xsd:dateTime .
  
  sub:temporalResolution a nt:LiteralPlaceholder;
    rdfs:label "Temporal resolution (optional, ISO 8601 duration format, e.g., P1D for daily, P1M for monthly)";
    nt:hasDatatype xsd:duration .
  
  # Define topic and dataset placeholders
  sub:topic a nt:GuidedChoicePlaceholder;
    rdfs:label "URI of concept or topic the sentence is about";
    nt:possibleValuesFromApi "http://purl.org/nanopub/api/find_signed_things?type=http%3A%2F%2Fwww.w3.org%2F2002%2F07%2Fowl%23Class&searchterm=",
      "https://www.wikidata.org/w/api.php?action=wbsearchentities&language=en&format=json&limit=5&search=" .
  
  sub:project a nt:GuidedChoicePlaceholder;
    rdfs:label "URI of a resource such as a Research Object RO-Crate or a nanopublication for related research project (optional)";
    nt:possibleValuesFromApi "https://w3id.org/np/l/nanopub-query-1.1/api/RAz6f1v82BCG0SjYMfHUe-m927VTVKdwvsuq1X7j1qcA8/find-things?type=https://schema.org/ResearchProject" .
  
  sub:dataset a nt:UriPlaceholder;
    rdfs:label "URI of nanopublication for related dataset (optional)" .
  
  # Define scientific paper placeholders
  sub:scientificPaper a nt:ExternalUriPlaceholder;
    rdfs:label "DOI (https://doi.org/10...) or other URL of the scientific paper (optional)" .
  
  sub:citationType a nt:RestrictedChoicePlaceholder;
    rdfs:label "Select the citation relationship type (optional)";
    nt:possibleValue <http://purl.org/spar/cito/cites>, <http://purl.org/spar/cito/citesAsSourceDocument>, 
      <http://purl.org/spar/cito/obtainsSupportFrom>, <http://purl.org/spar/cito/usesDataFrom>,
      <http://purl.org/spar/cito/usesMethodIn>, <http://purl.org/spar/cito/extends>,
      <http://purl.org/spar/cito/confirms>, <http://purl.org/spar/cito/supports> .
  
  sub:extractedText a nt:LiteralPlaceholder;
    rdfs:label "Text extracted from the paper (quote or paraphrase)" .
  
  sub:textChunk a nt:LocalResource;
    rdfs:label "Text chunk from paper" .
  
  sub:pageNumber a nt:LiteralPlaceholder;
    rdfs:label "Page number or section reference (e.g., 'p. 123', 'pp. 45-47', 'Table 2')";
    nt:hasRegex ".{1,50}" .
  
  sub:sectionTitle a nt:LiteralPlaceholder;
    rdfs:label "Section title or heading (e.g., 'Abstract', 'Results', 'Discussion', 'Figure 3 caption')";
    nt:hasRegex ".{1,200}" .
  
  sub:paragraphNumber a nt:LiteralPlaceholder;
    rdfs:label "Paragraph number or position within section (optional, e.g., 'paragraph 2', 'first sentence')";
    nt:hasRegex ".{1,100}" .
  
  sub:extractionType a nt:RestrictedChoicePlaceholder;
    rdfs:label "Type of text extraction";
    nt:possibleValue "direct quote", "paraphrase", "summary", "data point" .
  
  # Define the temporal period as a blank node
  sub:temporalPeriod a nt:LocalResource;
    rdfs:label "Temporal period" .
  
  # Define all statements
  sub:assertion dct:description """<p>This template allows you to express a research statement as an AIDA sentence while also capturing its spatial and temporal context, and optionally linking to scientific papers and specific text extracts.</p>

<p>AIDA sentences are:<p>

<ul>
<li><strong>Atomic:</strong> a sentence describing one thought that cannot be further broken down in a practical way</li>
<li><strong>Independent:</strong> a sentence that can stand on its own, without external references like \"this effect\" or \"we\"</li>
<li><strong>Declarative:</strong> a complete sentence ending with a full stop that could in theory be either true or false</li>
<li><strong>Absolute:</strong> a sentence describing the core of a claim ignoring the (un)certainty about its truth and ignoring how it was discovered (no \"probably\" or \"evaluation showed that\"); typically in present tense</li>
</ul>

<p>Additionally, you can specify:</p>
<ul>
<li><strong>Spatial Coverage:</strong> Where the research applies (geographic location, bounding box, or geometry)</li>
<li><strong>Temporal Coverage:</strong> When the research applies or was conducted</li>
<li><strong>Resolution:</strong> The precision of spatial and temporal measurements</li>
<li><strong>Scientific Paper:</strong> DOI or URL of the source paper</li>
<li><strong>Text Extract:</strong> Multiple specific quotes or paraphrases from the paper, each with precise location details (page, section, paragraph)</li>
</ul>

<p>You can find more information about AIDA sentences <a href=\"https://github.com/tkuhn/aida\" target=\"_blank\">here</a> and about CiTO citation types <a href=\"http://purl.org/spar/cito\" target=\"_blank\">here</a>.</p>""";
    a nt:AssertionTemplate;
    rdfs:label "Expressing a research statement as an AIDA sentence with spatial-temporal coverage and paper citations";
    nt:hasNanopubLabelPattern "AIDA sentence with context: ${aida}";
    nt:hasStatement sub:st0, sub:st1, sub:st2, sub:st3, sub:st4, sub:st5, sub:st6, sub:st7, sub:st8, sub:st9, sub:st10, sub:st11, sub:st12, sub:st13, sub:st14, sub:st15, sub:st16, sub:st17, sub:st18, sub:st19;
    nt:hasTag "Claims", "Spatiotemporal", "Geography", "Time", "Citations", "Papers";
    nt:hasTargetNanopubType <http://purl.org/petapico/o/hycl#AIDA-Sentence>, <http://purl.org/petapico/o/hycl>, <http://purl.org/spar/cito/cites>, <http://purl.org/spar/fabio/ScholarlyWork> .
  
  # Core AIDA sentence statements
  sub:st0 rdf:object <http://purl.org/petapico/o/hycl#AIDA-Sentence>;
    rdf:predicate rdf:type;
    rdf:subject sub:aida .
  
  sub:st1 rdf:object sub:topic;
    rdf:predicate schema:about;
    rdf:subject sub:aida;
    a nt:OptionalStatement, nt:RepeatableStatement .
  
  sub:st2 rdf:object sub:project;
    rdf:predicate <http://www.w3.org/2004/02/skos/core#related>;
    rdf:subject sub:aida;
    a nt:OptionalStatement .
  
  sub:st3 rdf:object sub:dataset;
    rdf:predicate <http://purl.org/spar/cito/obtainsSupportFrom>;
    rdf:subject sub:aida;
    a nt:OptionalStatement .
  
  # Spatial coverage statements  
  sub:st4 rdf:object sub:spatialCoverage;
    rdf:predicate dct:spatial;
    rdf:subject sub:aida;
    a nt:OptionalStatement .
  
  sub:st5 rdf:object sub:spatialResolution;
    rdf:predicate dcat:spatialResolutionInMeters;
    rdf:subject sub:aida;
    a nt:OptionalStatement .
  
  # Temporal coverage statements
  sub:st6 rdf:object sub:temporalPeriod;
    rdf:predicate dct:temporal;
    rdf:subject sub:aida;
    a nt:OptionalStatement .
  
  sub:st7 rdf:object dct:PeriodOfTime;
    rdf:predicate rdf:type;
    rdf:subject sub:temporalPeriod;
    a nt:OptionalStatement .
  
  sub:st8 rdf:object sub:temporalStart;
    rdf:predicate dcat:startDate;
    rdf:subject sub:temporalPeriod;
    a nt:OptionalStatement .
  
  sub:st9 rdf:object sub:temporalEnd;
    rdf:predicate dcat:endDate;
    rdf:subject sub:temporalPeriod;
    a nt:OptionalStatement .
  
  sub:st10 rdf:object sub:temporalResolution;
    rdf:predicate dcat:temporalResolution;
    rdf:subject sub:aida;
    a nt:OptionalStatement .
  
  # Scientific paper citation statements
  sub:st11 rdf:object <http://purl.org/spar/fabio/ScholarlyWork>;
    rdf:predicate rdf:type;
    rdf:subject sub:scientificPaper;
    a nt:OptionalStatement .
  
  sub:st12 rdf:object sub:scientificPaper;
    rdf:predicate sub:citationType;
    rdf:subject sub:aida;
    a nt:OptionalStatement .
  
  # Text extraction statements (repeatable for multiple extracts)
  sub:st13 rdf:object sub:textChunk;
    rdf:predicate <http://purl.org/spar/cito/includesQuotationFrom>;
    rdf:subject sub:aida;
    a nt:OptionalStatement, nt:RepeatableStatement .
  
  sub:st14 rdf:object <http://purl.org/spar/doco/TextChunk>;
    rdf:predicate rdf:type;
    rdf:subject sub:textChunk;
    a nt:OptionalStatement, nt:RepeatableStatement .
  
  sub:st15 rdf:object sub:extractedText;
    rdf:predicate rdfs:comment;
    rdf:subject sub:textChunk;
    a nt:OptionalStatement, nt:RepeatableStatement .
  
  sub:st16 rdf:object sub:scientificPaper;
    rdf:predicate dct:isPartOf;
    rdf:subject sub:textChunk;
    a nt:OptionalStatement, nt:RepeatableStatement .
  
  sub:st17 rdf:object sub:pageNumber;
    rdf:predicate <http://purl.org/spar/fabio/hasPageNumber>;
    rdf:subject sub:textChunk;
    a nt:OptionalStatement, nt:RepeatableStatement .
  
  sub:st18 rdf:object sub:sectionTitle;
    rdf:predicate dct:title;
    rdf:subject sub:textChunk;
    a nt:OptionalStatement, nt:RepeatableStatement .
  
  sub:st19 rdf:object sub:paragraphNumber;
    rdf:predicate <http://purl.org/spar/doco/hasContent>;
    rdf:subject sub:textChunk;
    a nt:OptionalStatement, nt:RepeatableStatement .
}

sub:provenance {
  sub:assertion prov:wasAttributedTo orcid:0000-0002-1784-2920 .
}

sub:pubinfo {
  orcid:0000-0002-1784-2920 foaf:name "Anne Fouilloux" .
  
  sub:sig npx:hasAlgorithm "RSA";
    npx:hasPublicKey "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDWv2pJnmDsBOq8OlT1aSvYXSuWT34WOp4FYqEzdnn2F0kqzcFevBqWGZDxJWC0lqCrDEuNfp2QFyPe/+nES9dlHGYIhqPi68fwK6ZiNUotRFxXou+rjFznVvUxtCL8Ede79EBHwWN61QtwSIcU12bLoZsNPFlqQASQ93BJuKlihwIDAQAB";
    npx:hasSignature "ES2r2hzEe1eCfIOPjQcCKOtvVo4J4t7PZSn4tGEgn5+RyBEm7qOGgqB8WHxB0C6KPr6tYvQ7db1u/KvHwp/oHoc/DDeFvxhlJmOD23tdgycuSgzyCG74Ze9UUu//07JgVbopyZBgCzIY7mhsY8iMgdSMziQubUzY+R+QogwElMk=";
    npx:hasSignatureTarget this:;
    npx:signedBy orcid:0000-0002-1784-2920 .
  
  this: dct:created "2025-05-24T12:00:00.000Z"^^xsd:dateTime;
    dct:creator orcid:0000-0002-1784-2920;
    dct:license <https://creativecommons.org/licenses/by/4.0/>;
    npx:wasCreatedAt <https://nanodash.knowledgepixels.com/>;
    rdfs:label "Template: Expressing a research statement as an AIDA sentence with spatial-temporal coverage and paper citations";
    nt:wasCreatedFromProvenanceTemplate <https://w3id.org/np/RA7lSq6MuK_TIC6JMSHvLtee3lpLoZDOqLJCLXevnrPoU>;
    nt:wasCreatedFromPubinfoTemplate <https://w3id.org/np/RA0J4vUn_dekg-U1kK3AOEt02p9mT2WO03uGxLDec1jLw>,
      <https://w3id.org/np/RAukAcWHRDlkqxk7H2XNSegc1WnHI569INvNr-xdptDGI>;
    nt:wasCreatedFromTemplate <https://w3id.org/np/RA4fmfVFULMP50FqDFX8fEMn66uDF07vXKFXh_L9aoQKE> .
}
```

## Template following patent claim 

This template enables researchers and patent professionals to create nanopublications that capture patent claims in a structured, machine-readable format while maintaining the formal structure required by patent law e.g. follow [https://www.wipo.int/edocs/mdocs/aspac/en/wipo_ip_phl_16/wipo_ip_phl_16_t5.pdf](https://www.wipo.int/edocs/mdocs/aspac/en/wipo_ip_phl_16/wipo_ip_phl_16_t5.pdf).


```
@prefix np: <http://www.nanopub.org/nschema#> .
@prefix npx: <http://purl.org/nanopub/x/> .
@prefix ns1: <http://schema.org/> .
@prefix orcid: <https://orcid.org/> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix sub: <http://purl.org/np/RAtfwFIRcAaIhzE681sa9MDJpQ6tBzKGj9mDmbnHemWe8#> .
@prefix this: <http://purl.org/np/RAtfwFIRcAaIhzE681sa9MDJpQ6tBzKGj9mDmbnHemWe8> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

sub:provenance {
    sub:assertion prov:generatedAtTime "2025-05-29T17:42:06.958894"^^xsd:dateTime .
}

sub:Head {
    this: a np:Nanopublication ;
        np:hasAssertion sub:assertion ;
        np:hasProvenance sub:provenance ;
        np:hasPublicationInfo sub:pubinfo .
}

sub:pubinfo {
    sub:sig npx:hasAlgorithm "RSA" ;
        npx:hasPublicKey "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAzu1mVoEI1kEjUkCSY0wbXW7sk8wQZdD2STFFM9f8Mg3oH9dIC9asPAcawftcHKUKkkzAjVzlq53drCsPsShB504i5jW2GGeMoMAfkuCJaC7jMjI+NB1idsvXhr1mdS4VnNtluY+kTzbX8x2gNI0zDm9rk9TUjltxjI6nKFL3qOaAPC/H3amoiJzNXPjDo8p05ko4bbLdOTw634jX1ifln/auzC32bEznkxCti+8vULA4xeeUHPePLAk/8iokk4FObZ4rLNri48gz0QOsi4MNW8mSAo51eKzgOFhzNGLki+cn5C+7In5Mw7Jk9EZzgvxZZcSGIL8F5OgpnycHEb95EQIDAQAB" ;
        npx:hasSignature "QAhbYB+KMefsYABCP4phJMVUu0YB+7lsXx4c8eqVaTys8uQuJUzeOWkzcpOr4RnrVeJTqKfxugcHZe08ouK9UWGjbaPkHGhWM8cSVVQBBNVSPxob/izsgM0vE8Z3VKYu0tSDtSAxVoj30fv64JV+YmFoABeIz1OKh2nUsOCox0lEYsS4WEcTJ6rzix5q4Of+urLQvIXHIY2lAAjQ1Hbp4R44J1Syu7wkaGEq8+uFscPNTTt5GLdS0s1OYTFYllpnQEEnOSG6DCv37XgdQJgkpPJ6YgqR0JxaqePXGDcscXIJnZhMAlrLsod84w6SGXQdlc3DCJ4nARHFfzgj7i5RuA==" ;
        npx:hasSignatureTarget this: ;
        npx:signedBy orcid:0000-0002-1784-2920 .

    this: prov:wasAttributedTo orcid:0000-0002-1784-2920 .
}

sub:assertion {
    sub:_patent_claim_1 a ns1:CreativeWork ;
        rdfs:label "Patent Claim 1" ;
        ns1:additionalProperty sub:_transitional_phrase_1 ;
        ns1:category "An apparatus" ;
        ns1:description "a handle; and a head portion connected to the handle." ;
        ns1:position 1 .

    sub:_transitional_phrase_1 a ns1:PropertyValue ;
        ns1:name "transitionalPhrase" ;
        ns1:value "comprising" .
}
```
