from tokenize import TokenError
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from phonenumber_field.serializerfields import PhoneNumberField
from django.contrib.auth import authenticate
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework_simplejwt.utils import aware_utcnow


class LoginSerializer(serializers.Serializer):
    phone_number = PhoneNumberField()
    password = serializers.CharField(write_only=True)
    tokens = serializers.SerializerMethodField(read_only=True)

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')

        user = authenticate(username=phone_number, password=password)
        print(user)

        if not user:
            raise serializers.ValidationError({"xatolik": "Telefon raqami yoki parol noto‘g‘ri."})
        if not user.is_active:
            raise serializers.ValidationError({"xatolik": "Foydalanuvchi bloklangan."})

        self.user = user
        return attrs

    def get_tokens(self, obj):
        user = self.user
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField(required=False)

    def validate(self, attrs):
        refresh_token_str = attrs.get("refresh")
        self.access_token_str = attrs.get("access")

        try:
            # blacklistni tekshirmasdan tokenni parse qilish
            self.refresh_token = RefreshToken(refresh_token_str, verify=False)

            # Endi token turini tekshiramiz
            if self.refresh_token.payload.get("token_type") != "refresh":
                raise serializers.ValidationError("Noto‘g‘ri token turi")

            # O'zimiz blacklistda ekanligini tekshiramiz
            if BlacklistedToken.objects.filter(token__token=refresh_token_str).exists():
                raise serializers.ValidationError("Token allaqachon blacklist qilingan")

            return attrs

        except TokenError as e:
            raise serializers.ValidationError(
                f"Token noto‘g‘ri yoki bekor qilingan: {str(e)}"
            )

    def save(self, **kwargs):
        try:
            # Refresh tokenni blacklistga qo‘shish
            self.refresh_token.blacklist()

            # Agar access token mavjud bo‘lsa, uni ham blacklistga qo‘shamiz
            if self.access_token_str:
                try:
                    access_token = AccessToken(self.access_token_str)
                    outstanding = OutstandingToken.objects.filter(token=str(access_token)).first()
                    if outstanding and not BlacklistedToken.objects.filter(token=outstanding).exists():
                        BlacklistedToken.objects.create(token=outstanding, expires_at=aware_utcnow())
                except TokenError as e:
                    # Agar access token noto‘g‘ri bo‘lsa, uni blacklistga qo‘shmaymiz, lekin logout davom etadi
                    print(f"Access token xatosi: {str(e)}")
                    pass

            return {"success": True, "message": "Muvaffaqiyatli chiqildi"}

        except Exception as e:
            return {"success": False, "error": str(e)}
