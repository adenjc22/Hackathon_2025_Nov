from typing import Any, Optional

def get_user_id(current_user: Optional[Any]) -> Optional[int]:
    return getattr(current_user, "id", None)