# Limb 매핑
velocity_to_limb = {
    10: ["Right Leg"],
    20: ["Left Leg"],
    30: ["Right Arm"],
    40: ["Left Arm"],
    50: ["Left Leg", "Right Arm"]
}

# 드럼 좌표
drum_positions = {
    "Kick": (390, 385),
    "Snare": (205, 385),
    "Hi-hat": (150, 250),
    "Crash 1": (210, 150),
    "High Tom": (310, 270),
    "Middle Tom": (470, 270),
    "Low Tom": (585, 385),
    "Crash 2": (580, 150),
    "Ride Cymbal": (630, 250)
}
drum_positions.update({
    "Closed Hi-Hat": drum_positions["Hi-hat"],
    "Pedal Hi-Hat": drum_positions["Hi-hat"],
    "Open Hi-Hat": drum_positions["Hi-hat"]
})

# MIDI note -> Drum
NOTE_TO_DRUM = {
    36: "Kick",
    38: "Snare",
    41: "Low Tom",
    42: "Closed Hi-Hat",
    44: "Pedal Hi-Hat",
    46: "Open Hi-Hat",
    47: "Middle Tom",
    49: "Crash 1",
    50: "High Tom",
    51: "Ride Cymbal",
    57: "Crash 2"
}
