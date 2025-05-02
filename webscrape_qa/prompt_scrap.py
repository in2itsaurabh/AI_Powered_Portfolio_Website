
from langchain_core.prompts import ChatPromptTemplate
from home.llm_models import llm_gemini
# template = (
#     "You are tasked with extracting specific information from the following text content: {dom_content}. "
#     "Please follow these instructions carefully: \n\n"
#     "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
#     "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
#     "3. **Empty Response:** If no information matches the description, return an string ('unexpected question, feel free to ask another question')."
#     "4. **Direct Data Only:**According to User questions Give the response from there, with no other text. give in readable formate"
# )

# template = (
#     "Your task is to extract specific information from the provided text content: {dom_content}. "
#     "Please adhere to the following instructions carefully: \n\n"
#     "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
#     "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
#     "3. **Empty Response:** If no information matches the description, return the string: 'Unexpected question, feel free to ask another question.' "
#     "4. **Direct Data Only:** Respond according to the user's questions, ensuring the response is clear and in a readable and structure format to understand the user."
# )

template = (
    "Your task is to extract specific information from the provided text content: {dom_content}. "
    "Please adhere to the following instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return the string: 'Unexpected question, feel free to ask another question.' "
    "4. **User-Friendly Formatting:** Ensure the response is presented in a clear, well-organized format for easy understanding. "
    "   - Avoid presenting the response in a single line if it contains multiple pieces of information. "
    "   - Use bullet points, lists, or paragraphs as appropriate to make the information more readable. "
)

# gemini_llm= ChatGoogleGenerativeAI(
#                     model="gemini-2.0-flash-exp",
#                     temperature=0.7,
#                     top_p=1
#                 )
gemini_llm = llm_gemini()
def parse_with_llm(dom_chunks, parse_description):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | gemini_llm
    response = chain.invoke(
            {"dom_content": dom_chunks, "parse_description": parse_description}
        ).content
    # print("==============",response)
    return response