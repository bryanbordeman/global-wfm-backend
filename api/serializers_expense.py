from rest_framework import serializers
from expense.models import Expense, Mile, MileRate
from api.serializers_user import UserSerializer

class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        if isinstance(data, six.string_types):
            if 'data:' in data and ';base64,' in data:
                header, data = data.split(';base64,')

            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            file_extension = self.get_file_extension(file_name, decoded_file)
            complete_file_name = "%s.%s" % (file_name, file_extension, )
            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension

class  ExpenseSerializer(serializers.ModelSerializer):
    '''Expense serializer'''
    is_approved = serializers.ReadOnlyField()
    user = UserSerializer()
    class Meta:
        model = Expense
        fields = '__all__'
        depth = 1

class  CreateExpenseSerializer(serializers.ModelSerializer):
    '''Expense serializer'''
    is_approved = serializers.ReadOnlyField()
    receipt_pic = Base64ImageField(max_length=None, use_url=True)
    class Meta:
        model = Expense
        # fields = '__all__'
        exclude = ['user']


class ExpenseApprovedSerializer(serializers.ModelSerializer):
    '''Admin view only'''
    class Meta:
        model = Expense
        fields = ['id']
        read_only_fields = ['project', 'receipt_pic', 'merchant', 'price', 'notes', 'is_reimbursable', 'is_approved', 'date_purchased', 'date_created']

class  MileSerializer(serializers.ModelSerializer):
    '''Miles serializer'''
    user = UserSerializer()
    class Meta:
        model = Mile
        fields = ['id', 'user', 'project', 'miles', 'rate', 'price', 'notes', 'is_approved', 'date_purchased', 'date_created']
        depth = 1

class  CreateMileSerializer(serializers.ModelSerializer):
    '''Create Miles serializer'''
    is_approved = serializers.ReadOnlyField()
    class Meta:
        model = Mile
        # fields = '__all__'
        exclude = ['user']

class MileApprovedSerializer(serializers.ModelSerializer):
    '''Admin view only'''
    class Meta:
        model = Mile
        fields = ['id']
        read_only_fields = ['user', 'project', 'miles', 'rate', 'price', 'notes', 'is_approved', 'date_purchased', 'date_created']

class  MileRatesSerializer(serializers.ModelSerializer):
    '''Mile Rates serializer'''
    class Meta:
        model = MileRate
        fields = '__all__'