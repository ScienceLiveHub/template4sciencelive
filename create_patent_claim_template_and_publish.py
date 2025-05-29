import rdflib
from rdflib import BNode, Namespace
from nanopub import Nanopub, NanopubConf, Profile 
from pathlib import Path

# Constructing profile for publishing nanopublications
def create_memory_profile(name: str, orcid_id: str):
    """Create profile entirely in memory without file I/O"""
    profile = Profile(
        name=name,
        orcid_id=orcid_id
    )
    return profile


# namespaces
NPX = Namespace("http://purl.org/nanopub/x/")

# Load user profile (make sure you have set up your profile first)
#profile = load_profile()
# Set up Anne Fouilloux's profile
profile = create_memory_profile(
   name="Anne Fouilloux",
   orcid_id="https://orcid.org/0000-0002-1784-2920"
)
# 1. Create configuration
np_conf = NanopubConf(
    profile=profile,
    use_test_server=True,
    add_prov_generated_time=True,
    attribute_publication_to_profile=True,
)


# 2. Create the assertion graph for a patent claim
my_assertion = rdflib.Graph()

# Define namespaces
SCHEMA = rdflib.Namespace("http://schema.org/")

# Use BNode for the patent claim - nanopub will generate proper URI
patent_claim = BNode("patent_claim_1")

# Patent claim example: "An apparatus comprising a handle and a head portion"
my_assertion.add((
    patent_claim,
    rdflib.RDF.type,
    SCHEMA.CreativeWork
))

my_assertion.add((
    patent_claim,
    rdflib.RDFS.label,
    rdflib.Literal("Patent Claim 1")
))

my_assertion.add((
    patent_claim,
    SCHEMA.position,
    rdflib.Literal("1", datatype=rdflib.XSD.integer)
))

my_assertion.add((
    patent_claim,
    SCHEMA.category,
    rdflib.Literal("An apparatus")
))

my_assertion.add((
    patent_claim,
    SCHEMA.description,
    rdflib.Literal("a handle; and a head portion connected to the handle.")
))

# Add transitional phrase as structured property
transitional_prop = BNode("transitional_phrase_1")
my_assertion.add((
    patent_claim,
    SCHEMA.additionalProperty,
    transitional_prop
))

my_assertion.add((
    transitional_prop,
    rdflib.RDF.type,
    SCHEMA.PropertyValue
))

my_assertion.add((
    transitional_prop,
    SCHEMA.name,
    rdflib.Literal("transitionalPhrase")
))

my_assertion.add((
    transitional_prop,
    SCHEMA.value,
    rdflib.Literal("comprising")
))

# 3. Create and publish the nanopublication
# The introduces_concept parameter tells nanopub this BNode represents the main concept
np = Nanopub(
    conf=np_conf,
    assertion=my_assertion,
    introduces_concept=patent_claim  # This will get a proper URI when published
)
np.pubinfo.add((
    np.metadata.sig_uri,
    NPX["signedBy"],
    rdflib.URIRef(profile.orcid_id),
))


# Sign the nanopub
print("Signing nanopublication...")
np.sign()
print(f"✓ Signed nanopub: {np.source_uri}")
       
# Optionally publish (uncomment to publish to nanopub server)
#AF print("Publishing nanopublication...")
#AF np.publish()
        
# Save to file
output_file = Path("patent_claim_template.trig")
np.store(output_file, format='trig')
print(f"✓ Saved template to: {output_file}")
        
# Print the nanopub
print("\n" + "="*80)
print("GENERATED NANOPUBLICATION TEMPLATE:")
print("="*80)
print(np)
        
print(f"Published nanopublication: {np.source_uri}")
print(f"Patent claim URI: {np.concept_uri}")  # The actual URI of the patent claim
