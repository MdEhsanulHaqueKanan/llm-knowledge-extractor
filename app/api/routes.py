import json
from flask import Blueprint, request, jsonify
from app.database.models import db, Analysis
from app.core.llm_service import MockLLMService
from app.core.text_utils import extract_keywords

# A Blueprint is Flask's way of organizing a group of related views and other code.
# It helps in keeping our application modular.
api_bp = Blueprint('api', __name__)

# We create a single instance of our service to be used by the routes.
llm_service = MockLLMService()

@api_bp.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    texts = data.get('texts')

    # --- Robustness: Input Validation ---
    if not isinstance(texts, list) or not texts:
        return jsonify({"error": "Input must be a non-empty array of strings in the 'texts' field."}), 400

    results = []
    try:
        # --- Bonus: Batch Processing ---
        for text in texts:
            if not isinstance(text, str) or not text.strip():
                # For this prototype, we'll be strict and fail the whole batch if one item is invalid.
                return jsonify({"error": "All items in 'texts' must be non-empty strings."}), 400

            # --- Core Logic ---
            llm_result = llm_service.analyze_text(text)
            keywords = extract_keywords(text)
            
            structured_data = llm_result['structured_data']
            
            # --- Persistence ---
            analysis = Analysis(
                summary=llm_result['summary'],
                title=structured_data.get('title'),
                topics=json.dumps(structured_data.get('topics', [])), # Store list as JSON string
                sentiment=structured_data.get('sentiment'),
                keywords=json.dumps(keywords), # Store list as JSON string
                confidence=structured_data.get('confidence')
            )
            # Add to the session, but don't commit yet.
            db.session.add(analysis)
            results.append(analysis)
        
        # Commit all new analyses to the database in a single transaction.
        db.session.commit()
        
        # --- Prepare Response ---
        # Convert our SQLAlchemy objects to dictionaries for the JSON response.
        final_results = [r.to_dict() for r in results]
        
        # If the user sent only one item, return a single object, not a list with one item.
        return jsonify(final_results[0] if len(final_results) == 1 else final_results), 201

    # --- Robustness: Error Handling ---
    except ConnectionError as e:
        # This catches the deliberate failure from our mock service.
        db.session.rollback() # Important: undo any partial changes to the database.
        return jsonify({"error": str(e)}), 502  # 502 Bad Gateway is correct for an upstream service failure.
    except Exception as e:
        # Catch any other unexpected errors.
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred"}), 500

@api_bp.route('/search', methods=['GET'])
def search():
    query = request.args.get('topic')
    if not query:
        return jsonify({"error": "A 'topic' query parameter is required"}), 400

    # The search term looks for the query string inside the JSON arrays we stored.
    # e.g., it will match '..."prototyping"...' in the 'topics' column.
    search_term = f'%"{query}"%'
    
    results = Analysis.query.filter(
        db.or_( # Use OR to search in both topics and keywords
            Analysis.topics.like(search_term),
            Analysis.keywords.like(search_term)
        )
    ).all()

    return jsonify([r.to_dict() for r in results]), 200