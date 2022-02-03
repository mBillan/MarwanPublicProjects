import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class NumericFormField extends StatelessWidget{
  const NumericFormField({Key? key, required this.controller, required this.text, this.onChanged}) : super(key: key);
  final TextEditingController controller;
  final String text;
  final Function(String)? onChanged;

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: TextFormField(
        onChanged: (val) => onChanged!(val),
        controller: controller,
        // initialValue: "80",
        maxLength: 3,
        keyboardType: TextInputType.number,
        inputFormatters: <TextInputFormatter>[
          FilteringTextInputFormatter.digitsOnly
        ],
        // The validator receives the text that the user has entered.
        validator: (value) {
          if (value == null || value.isEmpty || int.parse(value) > 320 || int.parse(value) < 0) {
            return 'Please enter a valid BPM between 0-320';
          }

          return null;
        },
      ),
    );
  }


}