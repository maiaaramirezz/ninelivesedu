from fastapi import FastAPI, HTTPException
from src.schemas import VerificationRequest, VerificationResponse
from src.orchestator import VerificationGraph

app = FastAPI(title="Tutoring AI Microservice", version="1.0")
orchestrator = VerificationGraph()

@app.post("/api/v1/verify-tutor", response_model=VerificationResponse)
async def verify_tutor(request: VerificationRequest):
    """Endpoint principal consumido por Node.js"""
    
    # Preparamos el estado inicial del grafo
    initial_state = {
        "user_id": request.user_id,
        "file_url": request.file_url,
        "extracted_text": "",
        "is_valid": False,
        "confidence": 0.0,
        "reason": ""
    }
    
    try:
        # Ejecutamos el flujo de LangGraph
        result = orchestrator.graph.invoke(initial_state)
        
        # Formateamos la respuesta limpia
        return VerificationResponse(
            status="approved" if result["is_valid"] else "rejected",
            confidence=result["confidence"],
            reason=result["reason"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno IA: {str(e)}")