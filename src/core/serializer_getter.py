"""
all serializer getting logics
like:
 Get={}, Filter=[]
"""


class SerializerManipulationService:
    """
    SerializerManipulationService
    this SerializerManipulationService module used to manage all serializer getting logic for
    reuse all function bases codes
    """

    def __init__(self, **kwargs):
        self.type = kwargs.get('type', None)
        self.model_class = kwargs.get('model_class', None)
        self.serializer_class = kwargs.get('serializer_class', None)
        self.query_params_variables = kwargs.get('query_params_var', None)
        self.model_instance = kwargs.get('model_instance', None)
        self.request_data = kwargs.get('request_data', {})

    def get_serializer_data(self):
        """this get_single_serializer_data get single dict object data
        return: {}
        """
        try:
            instance = self.model_class.objects.get(
                **self.query_params_variables
            )
        except Exception as e:
            print(e)
            return []
        serializer = self.serializer_class(instance)
        return serializer.data if serializer else []

    def get_serializers_data(self):
        """this get_single_serializer_data get single dict object data
        return: {}
        """
        instance = self.model_class.objects.filter(
            **self.query_params_variables
        )
        if not instance:
            return []
        serializer = self.serializer_class(instance, many=True)
        return serializer.data if serializer else []

    def create_serializers_data(self):
        """this create_serializers_data create the data with request params
        return: {}
        """
        serializer = self.serializer_class(data=self.request_data)
        # serializer exception raise                                          
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data if serializer else []

    def update_serializers_data(self):
        """this update_serializers_data update the data with request params
        return: {}
        """
        serializer = self.serializer_class(
            self.model_instance,
            data=self.request_data,
            partial=True
        )
        # serializer exception raise                                          
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return serializer.data
        else:
            return []

    def __call__(self):
        """call all serializer helper functions """
        if self.type == '__single__':
            return self.get_serializer_data()
        if self.type == '__multiple__':
            return self.get_serializers_data()
        if self.type == '__create__':
            return self.create_serializers_data()
        if self.type == '__update__':
            return self.update_serializers_data()
