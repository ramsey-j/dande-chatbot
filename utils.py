import streamlit as st
from conversation import SQLConversation

def write_full_response(conversation: SQLConversation):
    """Create the full response, including query and explanation, results of the query, and the answer to the original question"""
    query_explanation = conversation.write_query()
    response = write_response(query_explanation, conversation)
    query, results, status = conversation.execute_query(response)

    if results is not None and not results.empty: 
        print(1)
        user_message = conversation.history.user_messages[-1]
        st.dataframe(results)
        _ = write_response(conversation.answer(user_message, query, results), st.empty())
    elif results is not None and results.empty:
        print(2)
        user_message = conversation.history.user_messages[-1]
        st.dataframe(results)
        _ = write_response(conversation.empty(user_message, query, results), st.empty())
    if status is not None:
        print(3)
        user_message = conversation.history.user_messages[-1]
        _ = write_response(conversation.error(user_message, query, status), st.empty())


def write_response(generator, conversation, results=None):
    """Construct response from the generator and append to conversation history"""
    response = ""
    resp_container = st.empty()
    for chunk in generator:
        response += (chunk.choices[0].delta.content or "")
        resp_container.markdown(response)
    response_msg = {"role": "assistant", "content": response}
    if results is not None:
        response_msg["results"] = results
    conversation.history.append(response_msg)
    return response

