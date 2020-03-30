# IKEA TRADFRI REMOTE

### An AppDaemon app to control lights and scenes with a Zigbee2MQTT connected TRÅDFRI remote

## E1524/E1810 remote (the round one):

| button |  |
|------------|----------------------------------------------------------------------------|
| power | toggle the state of the currently selected group |
| brightness up / down | change the brightness of the currently selected group |
| brightness up + power | set the brightness to 100% |
| brightness down + power | set the brightness to 1% |
| left arrow | cycle between groups |
| right arrow | turn on the next scene to all the groups (without turning on the lights which are switched off) |
| hold power | turn on/off all the groups |
| hold arrows | turn on/off a device and mark it as selected |

## E1743 dimmer:

| button |  |
|------------|----------------------------------------------------------------------------|
| on | toggle the state of the currently selected group |
| off | cycle between groups |
| hold on | change the brightness of the currently selected group |
| hold off | turn on the next scene to all the groups (without turning on the lights which are switched off) |

## Configuration example

This should be pasted in appdaemon/apps.yaml
```
remote_1:
  module: real_tradfri_remote
  class: TradfriRemote
  groups:
    group_1:
      - light.kitchen_ceiling_1
      - light.kitchen_ceiling_2
    group_2:
      - light.kitchen_spotlights
    group_3:
      - light.kitchen_led_strip
  zigbee_names: #mark group 1 as Zigbee group
    group_1:
      - 0x14b457fffe6792fa
      - 0xccccccfffe54400d
  right_arrow_mode: scenes
  scenes:
    - scene.kitchen_warm_white
    - scene.kitchen_cold_white
  hold_group: group.kitchen
  left_hold_device: 1
  right_hold_device: 2
  reset_after: 10
  remote: sensor.tradfri_remote_click
```

#### Warning: if you set `zigbee_names`, my [ha-zigbee-dimmer](https://github.com/notherealmarco/ha-zigbee-dimmer) script must be installed! Otherwise lights won't dimm.
#### If you are controlling non-zigbee devices, you need [this add-on](https://github.com/notherealmarco/appdaemon-light-dimmer) in order for the dimmer to work.

| key | value |
|------------|----------------------------------------------------------------------------|
| groups | a map of all the groups, each group is a list of lights |
| zigbee_names | zigbee2mqtt device id's or friendly names, set only if you use Zigbee lights. Group name must stay the same and 'groups' still needs to be set |
| right_arrow_mode | can be set to scenes or to input_select |
| scenes (use only if right_arrow_mode is set to scenes) | a list of scenes's entity id |
| input_select (use only if right_arrow_mode is set to input_select) | an input_select entity id, it cycles between the options |
| hold_group | a group to switch on/off when holding the power button |
| left_hold_device | group number to switch on / off (and mark as selected) when holding the left arrow. Can also be set to an entity_id like `light.kitchen_ceiling` |
| right_hold_device | group number to switch on / off (and mark as selected) when holding the right arrow. Can also be set to an entity_id like `light.kitchen_ceiling` |
| reset_after | idle time (in seconds) after which the first group will be marked as selected automatically |
| remote | tradfri remote's zigbee2mqtt entity (e.g. sensor.0xccccccfffe4062b9_click) |

## HACS installation

- Install AppDaemon, if you are on Hass.io you can use the add-on
- Add `https://github.com/notherealmarco/ha-tradfri-remote` custom repository (AppDaemon category)
- Paste the configuration at the end of the `appdaemon/apps.yaml`

## Manual installation

- Install AppDaemon, if you are on Hass.io you can use the add-on
- Clone or download the repo
- Paste `real_tradfri_remote` (`apps/real_tradfri_remote`) in `appdaemon/apps directory`
- Paste the configuration at the end of the `appdaemon/apps.yaml`
