class VideoModel {
  final String id;
  final String filename;
  final String filepath;
  final Duration duration;
  final int fileSize;
  final DateTime uploadedAt;
  final bool isProcessing;
  final String? outputPath;

  VideoModel({
    required this.id,
    required this.filename,
    required this.filepath,
    required this.duration,
    required this.fileSize,
    required this.uploadedAt,
    this.isProcessing = false,
    this.outputPath,
  });

  factory VideoModel.fromJson(Map<String, dynamic> json) {
    return VideoModel(
      id: json['id'] ?? '',
      filename: json['filename'] ?? 'unknown',
      filepath: json['filepath'] ?? '',
      duration: Duration(seconds: json['duration'] ?? 0),
      fileSize: json['file_size'] ?? 0,
      uploadedAt: DateTime.tryParse(json['uploaded_at'] ?? '') ?? DateTime.now(),
      isProcessing: json['is_processing'] ?? false,
      outputPath: json['output_path'],
    );
  }

  Map<String, dynamic> toJson() => {
    'id': id,
    'filename': filename,
    'filepath': filepath,
    'duration': duration.inSeconds,
    'file_size': fileSize,
    'uploaded_at': uploadedAt.toIso8601String(),
    'is_processing': isProcessing,
    'output_path': outputPath,
  };
}

class EditOperation {
  final String type; // 'text_detection', 'person_detection', 'add_text'
  final Map<String, dynamic> parameters;
  final DateTime createdAt;

  EditOperation({
    required this.type,
    required this.parameters,
    DateTime? createdAt,
  }) : createdAt = createdAt ?? DateTime.now();

  factory EditOperation.fromJson(Map<String, dynamic> json) {
    return EditOperation(
      type: json['type'] ?? '',
      parameters: json['parameters'] ?? {},
      createdAt: DateTime.tryParse(json['created_at'] ?? '') ?? DateTime.now(),
    );
  }

  Map<String, dynamic> toJson() => {
    'type': type,
    'parameters': parameters,
    'created_at': createdAt.toIso8601String(),
  };
}
