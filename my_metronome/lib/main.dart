import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:my_metronome/src/widgets.dart';
import 'package:quiver/async.dart';

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
  int tempo = 80;
  int metre = 4;
  int _ticksCounter = 0;

  late StreamSubscription<DateTime> _subscription;

  final _formKey = GlobalKey<FormState>();

  late final TextEditingController _tempoController;
  late final TextEditingController _metreController;
  List<Widget> _notes = [];

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
    _tempoController = TextEditingController(text: "80");
    _metreController = TextEditingController(text: "4");
  }

  @override
  void dispose() {
    _tempoController.dispose();
    _metreController.dispose();
    super.dispose();
  }

  void _togglePlay() {
    // Validate returns true if the form is valid, or false otherwise.
    if (_formKey.currentState!.validate()) {
      setState(() {
        Metronome _metronome =
            Metronome.epoch(Duration(milliseconds: (60000 / tempo).round()));

        if (_isPlaying) {
          // Stop the beats stream
          _subscription.cancel();
          // Reset the ticks counter
          _ticksCounter = 0;
          _notes = [];
          _isPlaying = false;

          // _bkgColor = Colors.red;
        } else {
          _subscription = _metronome.listen((d) {
            SystemSound.play(SystemSoundType.click);
            _updateNotes();
            _ticksCounter++;
          });
          _isPlaying = true;
        }
      });
    }
  }

  List<Widget> _updateNotes() {
    // int metre = int.parse(_metreController.text);
    int tick = _ticksCounter % metre;
    print("calling update notes $tick");

    setState(() {
      if (_notes.isEmpty || metre != _notes.length) {
        // Reset the whole list of notes since maybe the metre has changed
        _notes = [];
        // The first time building the notes widgets
        for (int i = 0; i < metre; i++) {
          _notes.add(const Icon(Icons.music_note_outlined,
              color: Colors.grey, size: 40));
        }
      } else {
        // Color the current note with green
        if (_ticksCounter != 0) {
          _notes[(_ticksCounter - 1) % metre] =
              const Icon(Icons.music_note, color: Colors.green, size: 45);
        }
        // Color the previous note with grey
        _notes[(_ticksCounter - 2) % metre] =
            const Icon(Icons.music_note_outlined, color: Colors.grey, size: 40);
      }
    });

    return _notes;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        leading: const Text("LOGO"),
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

  void onTempoChanged(double val) {
    setState(() {
      tempo = val.round();
    });

    // toggle play twice to update the subscription stream's tempo
    // and stay in the same playing state
    _togglePlay();
    _togglePlay();
  }

  Widget MainBody() {
    return Center(
      // widthFactor: 2,
      // Center is a layout widget. It takes a single child and positions it
      // in the middle of the parent.
      child: Form(
        key: _formKey,
        child: Column(
          mainAxisAlignment: MainAxisAlignment.spaceAround,
          children: <Widget>[
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: _updateNotes(),
            ),
            Column(
                mainAxisAlignment: MainAxisAlignment.start,
                children: <Widget>[
                  Text(
                    'Tempo is $tempo',
                    style: Theme.of(context).textTheme.headline4,
                  ),
                  Slider(
                    value: tempo.toDouble(),
                    onChanged: onTempoChanged,
                    min: 30,
                    max: 360,
                    // autofocus: true,
                    divisions: 330,
                    // label: "$tempo",
                  ),
                ]),
            // ),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text(
                  'Metre is   ',
                  style: Theme.of(context).textTheme.headline4,
                ),
                Expanded(
                  child:
                  SelectFormField(
                    controller: _metreController,
                    type: SelectFormFieldType.dropdown,
                    // or can be dialog
                    // initialValue: "4",
                    // by default choose 4/4
                    // icon: Icon(Icons.format_shapes),
                    labelText: 'Choose Metre',
                    items: _allowedMetres,
                    onChanged: (val) => setState(() {
                      metre = int.parse(_metreController.text);
                      _updateNotes();
                    }),
                    onSaved: (val) => print("Metre saved $val"),
                  ),
                ),
              ],
            ),
            const SizedBox(
              height: 30,
            ),
          ],
        ),
      ),
    );
  }

  void _showToast(BuildContext context, String text) {
    final scaffold = ScaffoldMessenger.of(context);

    scaffold.showSnackBar(
      SnackBar(
        content: Text(text),
        shape: const StadiumBorder(),
        backgroundColor: Colors.lightGreen,
        behavior: SnackBarBehavior.floating,
        duration: const Duration(milliseconds: 1000),
        width: 250,
        // action: SnackBarAction(label: 'UNDO', onPressed: scaffold.hideCurrentSnackBar),
        // elevation: 100,
        // animation: Animation,
      ),
    );
  }
}
