import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:my_metronome/src/widgets.dart';

// import 'package:fluttertoast/fluttertoast.dart';
import 'package:select_form_field/select_form_field.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'My Metronome App',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: const MyHomePage(title: 'My Metronome'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({Key? key, required this.title}) : super(key: key);

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  bool _isPlaying = false;
  final _formKey = GlobalKey<FormState>();
  // TODO: counts on which beat is currently playing.
  //  should add also a function to calculate and iterate over the BMP
  int _beatCounter = 0;

  late final TextEditingController _bpmController;
  late final TextEditingController _metreController;

  final List<Map<String, dynamic>> _allowedMetres = [
    {
      'value': 2,
      'label': '2/4',
    },
    {
      'value': 3,
      'label': '3/4',
    },
    {
      'value': 4,
      'label': '4/4',
    },
  ];

  @override
  void initState() {
    super.initState();
    _bpmController = TextEditingController(text: "80");
    _metreController = TextEditingController(text: "4");
  }

  @override
  void dispose() {
    _bpmController.dispose();
    _metreController.dispose();
    super.dispose();
  }

  void _togglePlay() {
    // Validate returns true if the form is valid, or false otherwise.
    if (_formKey.currentState!.validate()) {
      setState(() {
        _isPlaying = !_isPlaying;
      });
      String metronomeStatus = _isPlaying ? "on" : "off";
      String bpm = _bpmController.text;
      String metre = _metreController.text + "/4";
      _showToast(context, "Metronome is $metronomeStatus, BMP: $bpm, Metre: $metre");
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        leading: Text("LOGO"),
        // Here we take the value from the MyHomePage object that was created by
        // the App.build method, and use it to set our appbar title.
        actions: [
          FloatingActionButton(
            onPressed: () {
              _showToast(context, "opening my sounds!");
            },
            tooltip: 'Check my sounds',
            child: const Icon(Icons.music_video_outlined),
          ),
        ],
        title: Text(widget.title),
        actionsIconTheme: const IconThemeData(
          size: 35,
        ),
      ),
      body: MainBody(),
      floatingActionButton: FloatingActionButton(
        onPressed: _togglePlay,
        tooltip: 'Play/Pause',
        child: _isPlaying
            ? const Icon(Icons.pause)
            : const Icon(Icons.play_arrow_outlined),
      ),
    );
  }

  Widget MainBody() {
    return Center(
      // widthFactor: 2,
      // Center is a layout widget. It takes a single child and positions it
      // in the middle of the parent.
      child: Form(
        key: _formKey,
        child: Column(
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          children: <Widget>[
            Row(
              children: [
                Text(
                  'BPM:',
                  style: Theme.of(context).textTheme.headline4,
                ),
                NumericFormField(
                    controller: _bpmController,
                    text: "Please enter a valid BPM between 0-320"),
              ],
            ),
            Row(
              children: [
                Text(
                  'Metre:',
                  style: Theme.of(context).textTheme.headline4,
                ),
                Expanded(
                  child: SelectFormField(
                    controller: _metreController,
                    type: SelectFormFieldType.dropdown,
                    // or can be dialog
                    // initialValue: "4",
                    // by default choose 4/4
                    // icon: Icon(Icons.format_shapes),
                    labelText: 'Shape',
                    items: _allowedMetres,
                    onChanged: (val) => print(val),
                    onSaved: (val) => print(val),
                  ),
                ),
              ],
            ),
            Row(
              children: [
                Text(
                  'Beats playing',
                  style: Theme.of(context).textTheme.headline4,
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

/*
Form(
      key: _formKey,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          TextFormField(
            // The validator receives the text that the user has entered.
            validator: (value) {
              if (value == null || value.isEmpty) {
                return 'Please enter some text';
              }
              return null;
            },
          ),
          Padding(
            padding: const EdgeInsets.symmetric(vertical: 16.0),
            child: ElevatedButton(
              onPressed: () {
                // Validate returns true if the form is valid, or false otherwise.
                if (_formKey.currentState!.validate()) {
                  // If the form is valid, display a snackbar. In the real world,
                  // you'd often call a server or save the information in a database.
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(content: Text('Processing Data')),
                  );
                }
              },
              child: const Text('Submit'),
            ),
          ),
        ],
      ),
 */
  void _showToast(BuildContext context, String text) {
    final scaffold = ScaffoldMessenger.of(context);

    scaffold.showSnackBar(
      SnackBar(
        content: Text(text),
        shape: const StadiumBorder(),
        backgroundColor: Colors.lightGreen,
        behavior: SnackBarBehavior.floating,
        duration: const Duration(milliseconds: 1000),
        width: 200,
        // action: SnackBarAction(label: 'UNDO', onPressed: scaffold.hideCurrentSnackBar),
        // elevation: 100,
        // animation: Animation,
      ),
    );
  }
}
