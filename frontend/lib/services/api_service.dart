import 'package:dio/dio.dart';
import 'dart:io';

class ApiService {
  late Dio _dio;
  static const String baseUrl = 'http://localhost:8000/api';

  ApiService() {
    _dio = Dio(
      BaseOptions(
        baseUrl: baseUrl,
        connectTimeout: const Duration(seconds: 30),
        receiveTimeout: const Duration(seconds: 30),
        headers: {
          'Content-Type': 'application/json',
        },
      ),
    );

    // Add logging interceptor
    _dio.interceptors.add(
      LoggingInterceptor(),
    );
  }

  /// Upload a video file
  Future<Map<String, dynamic>> uploadVideo(File videoFile) async {
    try {
      final formData = FormData.fromMap({
        'file': await MultipartFile.fromFile(
          videoFile.path,
          filename: videoFile.path.split('/').last,
        ),
      });

      final response = await _dio.post(
        '/upload',
        data: formData,
        onSendProgress: (sent, total) {
          print('Upload progress: $sent / $total');
        },
      );

      if (response.statusCode == 200) {
        return response.data as Map<String, dynamic>;
      } else {
        throw Exception('Upload failed with status ${response.statusCode}');
      }
    } on DioException catch (e) {
      throw Exception('Upload error: ${e.message}');
    }
  }

  /// Process video with specified operation
  Future<Map<String, dynamic>> processVideo(
    String videoId,
    String operation, {
    Map<String, dynamic>? parameters,
  }) async {
    try {
      final response = await _dio.post(
        '/process',
        queryParameters: {
          'video_id': videoId,
          'operation': operation,
        },
        data: parameters ?? {},
      );

      if (response.statusCode == 200) {
        return response.data as Map<String, dynamic>;
      } else {
        throw Exception('Processing failed with status ${response.statusCode}');
      }
    } on DioException catch (e) {
      throw Exception('Processing error: ${e.message}');
    }
  }

  /// Export processed video
  Future<Map<String, dynamic>> exportVideo(String videoId) async {
    try {
      final response = await _dio.post(
        '/export',
        queryParameters: {
          'video_id': videoId,
        },
      );

      if (response.statusCode == 200) {
        return response.data as Map<String, dynamic>;
      } else {
        throw Exception('Export failed with status ${response.statusCode}');
      }
    } on DioException catch (e) {
      throw Exception('Export error: ${e.message}');
    }
  }

  /// Download video file
  Future<String> downloadVideo(String filename) async {
    try {
      final response = await _dio.get(
        '/download/$filename',
        options: Options(
          responseType: ResponseType.bytes,
        ),
      );

      if (response.statusCode == 200) {
        return response.data;
      } else {
        throw Exception('Download failed');
      }
    } on DioException catch (e) {
      throw Exception('Download error: ${e.message}');
    }
  }

  /// Get API health status
  Future<bool> getHealthStatus() async {
    try {
      final response = await _dio.get('/health');
      return response.statusCode == 200;
    } catch (e) {
      return false;
    }
  }
}

class LoggingInterceptor extends Interceptor {
  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) {
    print('==> REQUEST: ${options.method} ${options.path}');
    super.onRequest(options, handler);
  }

  @override
  void onResponse(Response response, ResponseInterceptorHandler handler) {
    print('<== RESPONSE: ${response.statusCode}');
    super.onResponse(response, handler);
  }

  @override
  void onError(DioException err, ErrorInterceptorHandler handler) {
    print('<!== ERROR: ${err.message}');
    super.onError(err, handler);
  }
}
