def chat_widget_history(request):
    return {"chat_widget_history": request.session.get("chat_history", [])}
