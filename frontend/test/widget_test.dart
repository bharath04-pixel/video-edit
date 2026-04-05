import 'package:flutter_test/flutter_test.dart';
import 'package:ai_video_editor/services/api_service.dart';

void main() {
  group('APIService Tests', () {
    late ApiService apiService;

    setUp(() {
      apiService = ApiService();
    });

    test('Health check endpoint returns 200', () async {
      final isHealthy = await apiService.getHealthStatus();
      expect(isHealthy, true);
    });

    test('API service initializes correctly', () {
      expect(apiService, isNotNull);
    });
  });
}
