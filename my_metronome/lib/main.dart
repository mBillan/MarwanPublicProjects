import 'dart:async';
import 'package:flutter/material.dart';
import 'package:quiver/async.dart';
import 'package:select_form_field/select_form_field.dart';
import 'package:audioplayers/audioplayers.dart';

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
  String sound = "basic";
  int _ticksCounter = 0;

  late StreamSubscription<DateTime> _subscription;

  final _formKey = GlobalKey<FormState>();

  late final TextEditingController _tempoController;
  late final TextEditingController _metreController;
  late final TextEditingController _soundController;
  List<Widget> _notes = [];

  List<Map<String, dynamic>> _allowedMetres = [];
  List<Map<String, dynamic>> _availableSounds = [];

  // AudioPlayers to enable using different beat sounds
  AudioCache audioCache = AudioCache();
  AudioPlayer advancedPlayer = AudioPlayer(mode: PlayerMode.LOW_LATENCY);
  String? localFilePath;
  String? localAudioCacheURI;

  playTicks(String audioFileAsset) {
    // Plays sounds from the assets directory
    audioCache.play(audioFileAsset).then((player) {
      if (player.state != PlayerState.PLAYING) {
        _showToast(context, "Unable to play the sounds");
      }
    });
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
            // SystemSound.play(SystemSoundType.click);
            String soundName = (_ticksCounter % metre == 0)
                ? '${sound}_tick.wav'
                : '${sound}_tack.wav';
            playTicks("sounds/$soundName");

            _updateNotes();
            _ticksCounter++;
          });
          _isPlaying = true;
        }
      });
    }
  }

  List<Widget> _updateNotes({double? maxWidth}) {
    maxWidth = ((maxWidth != null) ? maxWidth : 400) - 20;
    double? iconSize = maxWidth / metre;

    setState(() {
      if (_notes.isEmpty || metre != _notes.length) {
        // Reset the whole list of notes since maybe the metre has changed
        _notes = [];
        // The first time building the notes widgets
        for (int i = 0; i < metre; i++) {
          _notes.add(Icon(Icons.music_note_outlined,
              color: Colors.grey, size: iconSize));
        }
      } else {
        // Color the current note with green
        if (_ticksCounter != 0) {
          _notes[(_ticksCounter - 1) % metre] =
              Icon(Icons.music_note, color: Colors.green, size: iconSize + 5);
        }
        // Color the previous note with grey
        _notes[(_ticksCounter - 2) % metre] =
            Icon(Icons.music_note_outlined, color: Colors.grey, size: iconSize);
      }
    });

    return _notes;
  }

  List<Map<String, dynamic>> _initMetres() {
    List<Map<String, dynamic>> allowedMetres = [];
    int maxMetre = 12;
    for (int currMetre = 2; currMetre <= maxMetre; currMetre++) {
      allowedMetres.add({
        'value': currMetre,
        'label': '$currMetre/4',
      });
    }

    return allowedMetres;
  }

  List<Map<String, dynamic>> _initSounds() {
    // TODO: Add only the available sound files under assets/sounds

    List<Map<String, dynamic>> availableSounds = [
      {
        'value': 'basic',
        'label': 'basic',

        // we can also add:
        // 'icon': const Icon(Icons.sentiment_neutral),
      },
      {
        'value': 'bell',
        'label': 'bell',
      },
      {
        'value': 'clock',
        'label': 'clock',
      },
      {
        'value': 'drum',
        'label': 'drum',
      },
      {
        'value': 'muted',
        'label': 'muted',
      },
      {
        'value': 'wooden',
        'label': 'wooden',
      },
    ];

    return availableSounds;
  }

  void _onTempoChanged(double val) {
    setState(() {
      tempo = val.round();
    });

    // toggle play twice to update the subscription stream's tempo
    // and stay in the same playing state
    _togglePlay();
    _togglePlay();
  }

  void _onMetreChanged(String val) {
    setState(() {
      metre = int.parse(_metreController.text);
      _updateNotes();
    });

    // toggle play twice to reset the metronome
    _togglePlay();
    _togglePlay();
  }

  void _onSoundChanged(String val) {
    setState(() {
      sound = val;

      // Update the value of _soundController manually to sync all the instances
      // of the widgets that use this controller
      // mainly because PopupMenuButton doesn't update the have a controller
      _soundController.text = sound;
    });

    // toggle play twice to reset the metronome
    _togglePlay();
    _togglePlay();
  }

  @override
  void initState() {
    super.initState();
    _tempoController = TextEditingController(text: "$tempo");
    _metreController = TextEditingController(text: "$metre");
    _soundController = TextEditingController(text: sound);

    _allowedMetres = _initMetres();
    _availableSounds = _initSounds();
  }

  @override
  void dispose() {
    _tempoController.dispose();
    _metreController.dispose();
    _soundController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        leading: const Image(
            image: AssetImage('assets/images/my_metronome_app_logo.png')),
        title: Text(widget.title),
        actions: [
          FloatingActionButton(
            onPressed: () {},
            child: PopupMenuButton<String>(
              onSelected: _onSoundChanged,
              icon: const Icon(Icons.my_library_music),
              iconSize: 35,
              tooltip: "Change sound",
              itemBuilder: (BuildContext context) {
                return _availableSounds.map((Map<String, dynamic> element) {
                  return PopupMenuItem(
                      value: element['value'].toString(),
                      child: Text(element['label'].toString()));
                }).toList();
              },
            ),
          ),
        ],
      ),
      body: mainBody(),
      floatingActionButton: FloatingActionButton(
        onPressed: _togglePlay,
        tooltip: 'Play/Pause',
        child: _isPlaying
            ? const Icon(Icons.pause)
            : const Icon(Icons.play_arrow_outlined),
      ),
    );
  }

  Widget mainBody() {
    return Container(
      // Add a background image
      decoration: const BoxDecoration(
        image: DecorationImage(
          opacity: 0.15,
          image: AssetImage("assets/images/my_metronome_app_logo.png"),
          fit: BoxFit.cover,
        ),
      ),
      child: Center(
        // widthFactor: 2,
        // Center is a layout widget. It takes a single child and positions it
        // in the middle of the parent.
        child: Form(
          key: _formKey,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: <Widget>[
              SizedBox(
                width: 400,
                height: 40,
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: _updateNotes(),
                ),
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
                      onChanged: _onTempoChanged,
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
                    'Metre    ',
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
                      labelText: 'Choose Metre',

                      items: _allowedMetres,
                      onChanged: _onMetreChanged,
                    ),
                  ),
                ],
              ),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text(
                    'Sound    ',
                    style: Theme.of(context).textTheme.headline4,
                  ),
                  Expanded(
                    child: SelectFormField(
                      controller: _soundController,
                      type: SelectFormFieldType.dropdown,
                      // or can be dialog
                      // initialValue: "4",
                      // by default choose 4/4
                      // icon: Icon(Icons.format_shapes),
                      labelText: 'Choose sound',
                      changeIcon: true,
                      items: _availableSounds,
                      onChanged: _onSoundChanged,
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
