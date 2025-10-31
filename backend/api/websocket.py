"""
WebSocket support for real-time chat
"""
from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, Set
import json
import logging
import asyncio

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manages WebSocket connections"""
    
    def __init__(self):
        # Active connections: session_id -> Set of WebSocket connections
        self.active_connections: Dict[str, Set[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, session_id: str):
        """Accept new WebSocket connection"""
        await websocket.accept()
        
        if session_id not in self.active_connections:
            self.active_connections[session_id] = set()
        
        self.active_connections[session_id].add(websocket)
        logger.info(f"WebSocket connected: {session_id}")
    
    def disconnect(self, websocket: WebSocket, session_id: str):
        """Remove WebSocket connection"""
        if session_id in self.active_connections:
            self.active_connections[session_id].discard(websocket)
            
            # Clean up empty sessions
            if not self.active_connections[session_id]:
                del self.active_connections[session_id]
        
        logger.info(f"WebSocket disconnected: {session_id}")
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Send message to specific connection"""
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.error(f"Error sending message: {e}")
    
    async def broadcast_to_session(self, message: dict, session_id: str):
        """Broadcast message to all connections in a session"""
        if session_id not in self.active_connections:
            return
        
        disconnected = set()
        
        for connection in self.active_connections[session_id]:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting to {session_id}: {e}")
                disconnected.add(connection)
        
        # Remove disconnected connections
        for connection in disconnected:
            self.active_connections[session_id].discard(connection)
    
    def get_session_count(self) -> int:
        """Get number of active sessions"""
        return len(self.active_connections)
    
    def get_connection_count(self) -> int:
        """Get total number of connections"""
        return sum(len(conns) for conns in self.active_connections.values())


# Global connection manager
manager = ConnectionManager()


async def handle_websocket_message(
    websocket: WebSocket,
    session_id: str,
    data: dict,
    routing_service
):
    """
    Handle incoming WebSocket message
    
    Args:
        websocket: WebSocket connection
        session_id: Session ID
        data: Message data
        routing_service: RoutingService instance
    """
    try:
        message_type = data.get('type', 'chat')
        
        if message_type == 'chat':
            # Handle chat message
            query = data.get('message', '')
            
            if not query.strip():
                await manager.send_personal_message({
                    'type': 'error',
                    'error': 'Empty message'
                }, websocket)
                return
            
            # Send typing indicator
            await manager.send_personal_message({
                'type': 'typing',
                'status': 'start'
            }, websocket)
            
            # Process query
            from core.schemas import ChatRequest
            request = ChatRequest(
                message=query,
                session_id=session_id,
                use_feedback_learning=data.get('use_feedback_learning', True)
            )
            
            response = await routing_service.process_query(request)
            
            # Send typing indicator stop
            await manager.send_personal_message({
                'type': 'typing',
                'status': 'stop'
            }, websocket)
            
            # Send response
            await manager.send_personal_message({
                'type': 'response',
                'success': response.success,
                'solution': response.solution,
                'query': response.query,
                'routing': response.routing.dict() if response.routing else None,
                'metadata': response.metadata,
                'blocked': response.blocked,
                'error': response.error
            }, websocket)
        
        elif message_type == 'ping':
            # Handle ping
            await manager.send_personal_message({
                'type': 'pong'
            }, websocket)
        
        elif message_type == 'feedback':
            # Handle feedback submission
            await manager.send_personal_message({
                'type': 'feedback_received',
                'status': 'success'
            }, websocket)
        
        else:
            await manager.send_personal_message({
                'type': 'error',
                'error': f'Unknown message type: {message_type}'
            }, websocket)
    
    except Exception as e:
        logger.error(f"Error handling WebSocket message: {e}", exc_info=True)
        await manager.send_personal_message({
            'type': 'error',
            'error': str(e)
        }, websocket)


async def websocket_endpoint(
    websocket: WebSocket,
    session_id: str,
    routing_service
):
    """
    WebSocket endpoint handler
    
    Usage in routes.py:
    @router.websocket("/ws/{session_id}")
    async def websocket_route(
        websocket: WebSocket,
        session_id: str,
        routing_service: RoutingService = Depends(get_routing_service)
    ):
        await websocket_endpoint(websocket, session_id, routing_service)
    """
    await manager.connect(websocket, session_id)
    
    try:
        # Send welcome message
        await manager.send_personal_message({
            'type': 'connected',
            'session_id': session_id,
            'message': 'WebSocket connection established'
        }, websocket)
        
        # Listen for messages
        while True:
            # Receive message
            data = await websocket.receive_json()
            
            # Handle message
            await handle_websocket_message(
                websocket,
                session_id,
                data,
                routing_service
            )
    
    except WebSocketDisconnect:
        manager.disconnect(websocket, session_id)
        logger.info(f"Client {session_id} disconnected normally")
    
    except Exception as e:
        logger.error(f"WebSocket error for {session_id}: {e}", exc_info=True)
        manager.disconnect(websocket, session_id)


# Health check for WebSocket
def get_websocket_stats() -> dict:
    """Get WebSocket connection statistics"""
    return {
        'active_sessions': manager.get_session_count(),
        'total_connections': manager.get_connection_count(),
        'status': 'healthy'
    }