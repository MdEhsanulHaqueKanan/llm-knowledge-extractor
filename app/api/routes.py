import json
from flask import Blueprint, request, jsonify
from app.database.models import db, Analysis
from app.core.llm_service import MockLLMService
from app.core.text_utils import extract_keywords

api_bp = Blueprint('api', __name__)
llm_service = MockLLMService()

@api_bp.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    texts = data.get('texts')

    # --- Input Validation ---
    if not isinstance(texts, list) or not texts:
        return jsonify({"error": "Input must be a non-empty array of strings in the 'texts' field."}), 400

    results = []
    try:
        # --- Batch Processing Logic ---
        for text in texts:
            if not isinstance(text, str) or not text.strip():
                return jsonify({"error": "All items in 'texts' must be non-empty strings."}), 400

            llm_result = llm_service.analyze_text(text)
            keywords = extract_keywords(text)
            structured_data = llm_result['structured_data']
            
            analysis = Analysis(
                summary=llm_result['summary'],
                title=structured_data.get('title'),
                topics=json.dumps(structured_data.get('topics', [])),
                sentiment=structured_data.get('sentiment'),
                keywords=json.dumps(keywords),
                confidence=structured_data.get('confidence')
            )
            db.session.add(analysis)
            results.append(analysis)
        
        # Commit all new analyses to the database in a single transaction.
        db.session.commit()
        
        final_results = [r.to_dict() for r in results]
        
        # Return a single object for a single-item request, otherwise return the full list.
        return jsonify(final_results[0] if len(final_results) == 1 else final_results), 201

    # --- Error Handling ---
    except ConnectionError as e:
        db.session.rollback()
        # 502 Bad Gateway is appropriate for an upstream service failure.
        return jsonify({"error": str(e)}), 502
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred"}), 500

@api_bp.route('/search', methods=['GET'])
def search():
    query = request.args.get('topic')
    if not query:
        return jsonify({"error": "A 'topic' query parameter is required"}), 400

    # Search for the query term inside the JSON-stringified topics and keywords.
    search_term = f'%"{query}"%'
    
    results = Analysis.query.filter(
        db.or_(
            Analysis.topics.like(search_term),
            Analysis.keywords.like(search_term)
        )
    ).all()

    return jsonify([r.to_dict() for r in results]), 200