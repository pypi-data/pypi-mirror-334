from ai_chunking import RecursiveTextSplitter, AutoAIChunker, SemanticTextChunker, SectionBasedSemanticChunker

# Test the SectionBasedSemanticChunker
chunker = SectionBasedSemanticChunker()
chunks = chunker.chunk_documents([
    "/Users/sakshammittal/Documents/Nexla OpenSource GitHub/ai-chunking/temp/input/financebench/3M_2015_10K/3M_2015_10K.md",
])
print("SectionBasedSemanticChunker", len(chunks))

# chunker = AutoAIChunker()
# chunks = chunker.chunk_documents([
#     "/Users/sakshammittal/Documents/Nexla OpenSource GitHub/ai-chunking/temp/input/financebench/3M_2015_10K/3M_2015_10K.md",
# ])
# print("AutoAIChunker", len(chunks))



