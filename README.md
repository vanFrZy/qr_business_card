## QR Business card generator

Basic qr code business cards to help save the planet by not printing them on paper

### Usage
Run the script with
```bash
python qr_code_generator.py example.json
```

Using `example.json` file will result in the following
```json
{
  "name": "example",
  "position": "tester",
  "email": "example@test.com",
  "website": "example.com",
  "pixel_color": [
    0,
    0,
    0
  ],
  "background_color": [
    255,
    255,
    255
  ]
}
```
![example card](example.png)

This also works for companies who want to make business cards for their employees.

Consider this example in `acme.json`:
```json
{
  "members": [
    {
      "name": "bob",
      "position": "tester",
      "email": "bob@test.com",
      "website": "example.com",
      "logo": "logo_rr.png",
      "pixel_color": [
        0,
        0,
        0
      ],
      "background_color": [
        255,
        255,
        255
      ]
    },
    {
      "name": "alice",
      "position": "tester",
      "email": "alice@test.com",
      "website": "example.com",
      "logo": "logo_rr.png",
      "pixel_color": [
        38,
        60,
        90
      ],
      "background_color": [
        249,
        200,
        103
      ]
    }
  ]
}
```

Running 
```bash
python qr_code_generator.py acme.json
``` 
will result in the following qr codes:


![example card](alice.png)
![example card](bob.png)


