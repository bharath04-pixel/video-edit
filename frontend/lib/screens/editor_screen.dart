import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../services/api_service.dart';

class EditorScreen extends StatefulWidget {
  final String videoId;
  final String videoPath;

  const EditorScreen({
    Key? key,
    required this.videoId,
    required this.videoPath,
  }) : super(key: key);

  @override
  State<EditorScreen> createState() => _EditorScreenState();
}

class _EditorScreenState extends State<EditorScreen> {
  final ApiService _apiService = ApiService();
  bool _isProcessing = false;
  String _selectedOperation = 'text_detection';
  Map<String, dynamic> _analysisResults = {};

  Future<void> _processVideo(String operation) async {
    setState(() {
      _isProcessing = true;
      _selectedOperation = operation;
    });

    try {
      final results = await _apiService.processVideo(
        widget.videoId,
        operation,
      );

      setState(() {
        _analysisResults = results;
      });

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Processing complete!')),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error: $e')),
        );
      }
    } finally {
      if (mounted) {
        setState(() {
          _isProcessing = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
          'Edit Video',
          style: GoogleFonts.poppins(fontWeight: FontWeight.bold),
        ),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () => Navigator.pop(context),
        ),
      ),
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [Color(0xFF0F0F0F), Color(0xFF1A1A1A)],
          ),
        ),
        child: SingleChildScrollView(
          child: Padding(
            padding: const EdgeInsets.all(20),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Video Preview
                Container(
                  width: double.infinity,
                  height: 200,
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(15),
                    color: Colors.grey[900],
                    border: Border.all(color: Colors.grey[800]!),
                  ),
                  child: const Center(
                    child: Icon(
                      Icons.play_circle_outline,
                      size: 60,
                      color: Color(0xFF1DB954),
                    ),
                  ),
                ),
                const SizedBox(height: 30),

                // Analysis Operations
                Text(
                  'Analysis Options',
                  style: GoogleFonts.poppins(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 15),

                // Text Detection Button
                _buildOperationButton(
                  icon: '🔤',
                  title: 'Text Detection',
                  description: 'Detect text in video frames',
                  onPressed: () => _processVideo('text_detection'),
                  isActive: _selectedOperation == 'text_detection',
                  isLoading: _isProcessing && _selectedOperation == 'text_detection',
                ),
                const SizedBox(height: 10),

                // Person Detection Button
                _buildOperationButton(
                  icon: '👤',
                  title: 'Person Detection',
                  description: 'Find people in the video',
                  onPressed: () => _processVideo('person_detection'),
                  isActive: _selectedOperation == 'person_detection',
                  isLoading: _isProcessing && _selectedOperation == 'person_detection',
                ),
                const SizedBox(height: 10),

                // Metadata Extraction Button
                _buildOperationButton(
                  icon: '📊',
                  title: 'Extract Metadata',
                  description: 'Get video information',
                  onPressed: () => _processVideo('extract_metadata'),
                  isActive: _selectedOperation == 'extract_metadata',
                  isLoading: _isProcessing && _selectedOperation == 'extract_metadata',
                ),

                const SizedBox(height: 30),

                // Results Section
                if (_analysisResults.isNotEmpty) ...[
                  Text(
                    'Analysis Results',
                    style: GoogleFonts.poppins(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 15),
                  Container(
                    width: double.infinity,
                    padding: const EdgeInsets.all(15),
                    decoration: BoxDecoration(
                      color: Colors.grey[900],
                      borderRadius: BorderRadius.circular(10),
                      border: Border.all(color: Colors.grey[800]!),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        ..._analysisResults.entries.map(
                          (entry) => Padding(
                            padding: const EdgeInsets.symmetric(vertical: 5),
                            child: Row(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              children: [
                                Text(
                                  entry.key,
                                  style: GoogleFonts.poppins(
                                    fontSize: 12,
                                    color: Colors.grey[400],
                                  ),
                                ),
                                Text(
                                  entry.value.toString(),
                                  style: GoogleFonts.poppins(
                                    fontSize: 12,
                                    color: const Color(0xFF1DB954),
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 30),
                ],

                // Export Button
                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton.icon(
                    onPressed: _isProcessing
                        ? null
                        : () {
                            // Navigate to preview
                            ScaffoldMessenger.of(context).showSnackBar(
                              const SnackBar(
                                content: Text('Video ready for export!'),
                              ),
                            );
                          },
                    icon: const Icon(Icons.check_circle),
                    label: const Text('Continue to Preview'),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: const Color(0xFF1DB954),
                      foregroundColor: Colors.white,
                      padding: const EdgeInsets.symmetric(vertical: 14),
                      disabledBackgroundColor: Colors.grey[700],
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildOperationButton({
    required String icon,
    required String title,
    required String description,
    required VoidCallback onPressed,
    required bool isActive,
    required bool isLoading,
  }) {
    return GestureDetector(
      onTap: isLoading ? null : onPressed,
      child: Container(
        padding: const EdgeInsets.all(15),
        decoration: BoxDecoration(
          color: isActive ? const Color(0xFF1DB954).withOpacity(0.1) : Colors.grey[900],
          borderRadius: BorderRadius.circular(12),
          border: Border.all(
            color: isActive ? const Color(0xFF1DB954) : Colors.grey[800]!,
          ),
        ),
        child: Row(
          children: [
            SizedBox(
              width: 50,
              child: Center(
                child: isLoading
                    ? const SizedBox(
                        width: 24,
                        height: 24,
                        child: CircularProgressIndicator(
                          strokeWidth: 2,
                          valueColor: AlwaysStoppedAnimation(
                            Color(0xFF1DB954),
                          ),
                        ),
                      )
                    : Text(icon, style: const TextStyle(fontSize: 28)),
              ),
            ),
            const SizedBox(width: 15),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    title,
                    style: GoogleFonts.poppins(
                      fontWeight: FontWeight.bold,
                      fontSize: 14,
                    ),
                  ),
                  const SizedBox(height: 3),
                  Text(
                    description,
                    style: GoogleFonts.poppins(
                      fontSize: 11,
                      color: Colors.grey[400],
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(width: 10),
            Icon(
              Icons.arrow_forward_ios,
              size: 16,
              color: isActive ? const Color(0xFF1DB954) : Colors.grey[600],
            ),
          ],
        ),
      ),
    );
  }
}
