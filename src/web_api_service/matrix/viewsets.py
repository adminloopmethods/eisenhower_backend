from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from rest_framework_tracking.mixins import LoggingMixin

from core.api_response_parser import APIResponseParser
from core.messages import API_RESPONSE_MSG

from web_api_service.matrix.services import MatrixDashboardService


class DashboardApi(LoggingMixin, APIView):
    """
    DashboardApi
    usage: this endpoint used to get the all task counts with of logic matrix algo 
    path: /api/v1/matrix/dashboard/
    Methods: GET
    Authorization: YES
    Response:{
        "matrix_config_data": [
            {
                "id": "0f167aea-92b0-46a4-bbbe-afc303e60f04",
                "color": "46jdasd",
                "task_rule": [
                    {
                        "id": "d42f814f-d8dd-408e-b0df-eaa736f7b257",
                        "rule_name": "Importance",
                        "priority_status": "High",
                        "description": ""
                    },
                    {
                        "id": "3e382852-9f38-4949-8488-13c1512c2506",
                        "rule_name": "Urgency",
                        "priority_status": "High",
                        "description": ""
                    }
                ],
                "task_count": "0",
                "created_at": "2022-08-19T07:20:53.615865Z",
                "updated_at": "2022-08-19T07:20:53.615897Z",
                "is_active": true,
                "matrix_rule_name": "Priority 1",
                "description": "",
                "created_by": 1,
                "updated_by": null
            },
            {
                "id": "1f9abea3-4255-45f3-86bc-267f14c5e618",
                "color": "#0000FF",
                "task_rule": [
                    {
                        "id": "d42f814f-d8dd-408e-b0df-eaa736f7b257",
                        "rule_name": "Importance",
                        "priority_status": "High",
                        "description": ""
                    },
                    {
                        "id": "1dcda2c0-8d4c-4fb8-bd1a-b1b0b9a0de59",
                        "rule_name": "Urgency",
                        "priority_status": "Low",
                        "description": ""
                    }
                ],
                "task_count": "0",
                "created_at": "2022-08-19T07:21:30.312938Z",
                "updated_at": "2022-08-19T07:21:38.547026Z",
                "is_active": true,
                "matrix_rule_name": "Priority 3",
                "description": "",
                "created_by": 1,
                "updated_by": 1
            },
            {
                "id": "d22f9544-5305-4027-ab4b-11e0b4a00db2",
                "color": "#0000FF",
                "task_rule": [
                    {
                        "id": "d42f814f-d8dd-408e-b0df-eaa736f7b257",
                        "rule_name": "Importance",
                        "priority_status": "High",
                        "description": ""
                    },
                    {
                        "id": "ecee1e32-a4b3-48e1-a666-bf6fe5fbbecb",
                        "rule_name": "Urgency",
                        "priority_status": "Medium",
                        "description": ""
                    }
                ],
                "task_count": "0",
                "created_at": "2022-08-19T07:21:10.709471Z",
                "updated_at": "2022-08-19T07:21:45.337065Z",
                "is_active": true,
                "matrix_rule_name": "Priority 2",
                "description": "",
                "created_by": 1,
                "updated_by": 1
            },
            {
                "id": "4a914fdb-3038-4740-b051-80dbc919232f",
                "color": "#0000FF",
                "task_rule": [
                    {
                        "id": "3cf730f7-d334-43bb-ab39-cbc8c3b0aeb5",
                        "rule_name": "Importance",
                        "priority_status": "Medium",
                        "description": ""
                    },
                    {
                        "id": "3e382852-9f38-4949-8488-13c1512c2506",
                        "rule_name": "Urgency",
                        "priority_status": "High",
                        "description": ""
                    }
                ],
                "task_count": "0",
                "created_at": "2022-08-19T07:22:01.370360Z",
                "updated_at": "2022-08-19T07:22:01.370394Z",
                "is_active": true,
                "matrix_rule_name": "Priority 4",
                "description": "",
                "created_by": 1,
                "updated_by": null
            },
            {
                "id": "f2ec2760-bc1f-4f6a-9787-2f5640a88dc9",
                "color": "#0000FF",
                "task_rule": [
                    {
                        "id": "3cf730f7-d334-43bb-ab39-cbc8c3b0aeb5",
                        "rule_name": "Importance",
                        "priority_status": "Medium",
                        "description": ""
                    },
                    {
                        "id": "ecee1e32-a4b3-48e1-a666-bf6fe5fbbecb",
                        "rule_name": "Urgency",
                        "priority_status": "Medium",
                        "description": ""
                    }
                ],
                "task_count": "0",
                "created_at": "2022-08-19T07:22:15.589082Z",
                "updated_at": "2022-08-19T07:22:15.589150Z",
                "is_active": true,
                "matrix_rule_name": "Priority 5",
                "description": "",
                "created_by": 1,
                "updated_by": null
            },
            {
                "id": "a32a12f2-0e94-4fb0-af5a-5728fa72ab0f",
                "color": "#ADD8E6",
                "task_rule": [
                    {
                        "id": "3cf730f7-d334-43bb-ab39-cbc8c3b0aeb5",
                        "rule_name": "Importance",
                        "priority_status": "Medium",
                        "description": ""
                    },
                    {
                        "id": "1dcda2c0-8d4c-4fb8-bd1a-b1b0b9a0de59",
                        "rule_name": "Urgency",
                        "priority_status": "Low",
                        "description": ""
                    }
                ],
                "task_count": "0",
                "created_at": "2022-08-19T07:22:34.839012Z",
                "updated_at": "2022-08-19T07:22:34.839036Z",
                "is_active": true,
                "matrix_rule_name": "Priority 6",
                "description": "",
                "created_by": 1,
                "updated_by": null
            },
            {
                "id": "24d4c507-2f60-4c28-b12d-67e0ed386fdd",
                "color": "#ADD8E6",
                "task_rule": [
                    {
                        "id": "258db7e6-dcb6-4e83-bf6a-e8ea664597e0",
                        "rule_name": "Importance",
                        "priority_status": "Low",
                        "description": ""
                    },
                    {
                        "id": "3e382852-9f38-4949-8488-13c1512c2506",
                        "rule_name": "Urgency",
                        "priority_status": "High",
                        "description": ""
                    }
                ],
                "task_count": "0",
                "created_at": "2022-08-19T07:22:47.695909Z",
                "updated_at": "2022-08-19T07:22:47.695930Z",
                "is_active": true,
                "matrix_rule_name": "Priority 7",
                "description": "",
                "created_by": 1,
                "updated_by": null
            },
            {
                "id": "eb070eb9-a28f-45c3-a2c0-711c44178edd",
                "color": "#FFCCCB",
                "task_rule": [
                    {
                        "id": "258db7e6-dcb6-4e83-bf6a-e8ea664597e0",
                        "rule_name": "Importance",
                        "priority_status": "Low",
                        "description": ""
                    },
                    {
                        "id": "ecee1e32-a4b3-48e1-a666-bf6fe5fbbecb",
                        "rule_name": "Urgency",
                        "priority_status": "Medium",
                        "description": ""
                    }
                ],
                "task_count": "0",
                "created_at": "2022-08-19T07:23:04.332207Z",
                "updated_at": "2022-08-19T07:23:04.332236Z",
                "is_active": true,
                "matrix_rule_name": "Priority 8",
                "description": "",
                "created_by": 1,
                "updated_by": null
            },
            {
                "id": "2853b906-5e61-4094-8c86-89d6725bc919",
                "color": "#FFCCCB",
                "task_rule": [
                    {
                        "id": "258db7e6-dcb6-4e83-bf6a-e8ea664597e0",
                        "rule_name": "Importance",
                        "priority_status": "Low",
                        "description": ""
                    },
                    {
                        "id": "1dcda2c0-8d4c-4fb8-bd1a-b1b0b9a0de59",
                        "rule_name": "Urgency",
                        "priority_status": "Low",
                        "description": ""
                    }
                ],
                "task_count": "0",
                "created_at": "2022-08-19T07:23:15.340479Z",
                "updated_at": "2022-08-19T07:23:15.340530Z",
                "is_active": true,
                "matrix_rule_name": "Priority 9",
                "description": "",
                "created_by": 1,
                "updated_by": null
            }
        ],
        "success": true,
        "message": "Done"
    }
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        this get methods used to get the all matrix dashboard details
        """
        resp = MatrixDashboardService(auth_instance=request.user).dashboard_details()
        return APIResponseParser.response(**resp)
