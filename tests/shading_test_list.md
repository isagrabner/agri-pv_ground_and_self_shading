# List of tests for ground- and self-shading calculations

## Tests for the sun in overhead position 
**Elevation:** 90°\
**Azimuth:** - (irrelevant)

### Tracking system
- **Test 1:** Check if ground-shading for tracking system is correctly calculated\
    In this setup panels in the tracking system should be positioned horizontally, the sun projecting shade on the ground directly beneath them. The expected result is the total panel area in percent of the total field area.

- **Test 2:** Check if self-shading for tracking system is correctly calculated\
    In this setup panels in the tracking system should be positioned horizontally, fully eluminated by the sun. The expected result is 0% self-shading.

### Vertical system
- **Test 3:** Check if ground shading for vertical system is correctly calculated\
    With the panel depth being approximated as 0, the expected result is 0% ground-shading.

- **Test 4:** Check if self shading for vertical system is correctly calculated\
    The expected result is 0% self-shading.

### Standard system
- **Test 5:** Check if ground shading for standard system is correctly calculated\
    In this setup the expected ground-shading is the panel area as it appears in a bird's-eye view in percent of the total field area. The former is calculated by modifying the total panel area by the panel tilt.

- **Test 6:** Check if self shading for standard system is correctly calculated\
    The expected result is 0% self-shading.

### Overhead system
- **Test 7:** Check if ground shading for overhead system is correctly calculated\
    In this setup the expected ground-shading is the panel area as it appears in a bird's-eye view in percent of the total field area. The former is calculated by modifying the total panel area by the panel tilt.

- **Test 8:** Check if self shading for overhead system is correctly calculated\
    The expected result is 0% self-shading.
             
### Backtracking system
- **Test 9:** Check if ground shading for backtracking system is correctly calculated\
    In this setup panels in the backtracking system should be positioned horizontally, the sun projecting shade on the ground directly beneath them. The expected result is the total panel area in percent of the total field area.

- **Test 10:** Check if self shading for backtracking system is correctly calculated\
    In this setup panels in the tracking system should be positioned horizontally, fully eluminated by the sun. The expected result is 0% self-shading.

## Tests for the sun at the horizon (E)
**Elevation:** 10<sup>-10</sup> °\
**Azimuth:** 90°

### Tracking system
- **Test 11:** Check if ground shading for tracking system is correctly calculated\
    In this setup the sun beams should pass beneath the panels with no shading on the preset field. The expected value is 0% ground-shading.

- **Test 12:** Check if self shading for tracking system is correctly calculated\
    The sun should fully eluminate the first row of panels, with the panels in a vertical position. All rows behind the first one should be fully self-shaded. The expected value is the total panel area minus one row in percentage of the total panel area.

### Vertical system
- **Test 13:** Check if ground shading for vertical system is correctly calculated\
    In this setup the sun beams should pass beneath the panels with no shading on the preset field. The expected value is 0% ground-shading.

- **Test 14:** Check if self shading for vertical system is correctly calculated\
    The sun should fully eluminate the first row of panels. All rows behind the first one should be fully self-shaded. The expected value is the total panel area minus one row in percentage of the total panel area.

### Standard system
- **Test 15:** Check if ground shading for standard system is correctly calculated\
    In this setup the sun beams should pass beneath the panels with no shading on the preset field. The expected value is 0% ground-shading.

- **Test 16:** Check if self shading for standard system is correctly calculated\
    The sun beams should pass between the panels in this system. The expected value is 0% self-shading.

### Overhead system
- **Test 17:** Check if ground shading for overhead system is correctly calculated\
    In this setup the sun beams should pass beneath the panels with no shading on the preset field. The expected value is 0% ground-shading.

- **Test 18:** Check if self shading for overhead system is correctly calculated\
    The sun should fully eluminate the first row of panels. All rows behind the first one should be fully self-shaded. The expected value is the total panel area minus one row in percentage of the total panel area.

### Backtracking system
- **Test 19:** Check if ground shading for backtracking system is correctly calculated\
    In this setup the sun beams should pass beneath the panels with no shading on the preset field. The expected value is 0% ground-shading.

- **Test 20:** Check if self shading for backtracking system is correctly calculated\
    The panels should be positioned horizontally in this setup (to avoid self-shading). Leading to an expected value of 0% self-shading.

## Tests for the sun at the horizon (S)
**Elevation:** 10<sup>-10</sup> °\
**Azimuth:** 180°

### Tracking system
- **Test 21:** Check if ground shading for tracking system is correctly calculated\
    In this setup the sun beams should pass beneath the panels with no shading on the preset field. The expected value is 0% ground-shading.

- **Test 22:** Check if self shading for tracking system is correctly calculated\
    The sun beams should pass between the panels in this system. The expected value is 0% self-shading.

### Vertical system
- **Test 23:** Check if ground shading for vertical system is correctly calculated\
    In this setup the sun beams should pass beneath the panels with no shading on the preset field. The expected value is 0% ground-shading.

- **Test 24:** Check if self shading for vertical system is correctly calculated\
    The sun beams should pass between the panels in this system. The expected value is 0% self-shading.

### Standard system
- **Test 25:** Check if ground shading for standard system is correctly calculated\
    In this setup the sun beams should pass beneath the panels with no shading on the preset field. The expected value is 0% ground-shading.

- **Test 26:** Check if self shading for standard system is correctly calculated\
    The sun should fully eluminate the first row of panels. All rows behind the first one should be fully self-shaded. The expected value is the total panel area minus one row in percentage of the total panel area.

### Overhead system
- **Test 27:** Check if ground shading for overhead system is correctly calculated\
    In this setup the sun beams should pass beneath the panels with no shading on the preset field. The expected value is 0% ground-shading.

- **Test 28:** Check if self shading for overhead system is correctly calculated\
    The sun beams should pass between the panels in this system. The expected value is 0% self-shading.

### Backtracking system
- **Test 29:** Check if ground shading for backtracking system is correctly calculated\
    In this setup the sun beams should pass beneath the panels with no shading on the preset field. The expected value is 0% ground-shading.

- **Test 30:** Check if self shading for backtracking system is correctly calculated\
    The sun beams should pass between the panels in this system. The expected value is 0% self-shading.

## Tests for the sun at the horizon (W)
**Elevation:** 10<sup>-10</sup> °\
**Azimuth:** 270°

### Tracking system
- **Test 31:** Check if ground shading for tracking system is correctly calculated\
    In this setup the sun beams should pass beneath the panels with no shading on the preset field. The expected value is 0% ground-shading.

- **Test 32:** Check if self shading for tracking system is correctly calculated\
    The sun should fully eluminate the first row of panels, with the panels in a vertical position. All rows behind the first one should be fully self-shaded. The expected value is the total panel area minus one row in percentage of the total panel area.

### Vertical system
- **Test 33:** Check if ground shading for vertical system is correctly calculated\
    In this setup the sun beams should pass beneath the panels with no shading on the preset field. The expected value is 0% ground-shading.

- **Test 34:** Check if self shading for vertical system is correctly calculated\
    The sun should fully eluminate the first row of panels. All rows behind the first one should be fully self-shaded. The expected value is the total panel area minus one row in percentage of the total panel area.

### Standard system
- **Test 35:** Check if ground shading for standard system is correctly calculated\
    In this setup the sun beams should pass beneath the panels with no shading on the preset field. The expected value is 0% ground-shading.

- **Test 36:** Check if self shading for standard system is correctly calculated\
    The sun beams should pass between the panels in this system. The expected value is 0% self-shading.

### Overhead system
- **Test 37:** Check if ground shading for overhead system is correctly calculated\
    In this setup the sun beams should pass beneath the panels with no shading on the preset field. The expected value is 0% ground-shading.

- **Test 38:** Check if self shading for overhead system is correctly calculated\
    With the given panel tilt the sun should eluminate the back of the panels, leading to 100% self-shading by definition.

### Backtracking system
- **Test 39:** Check if ground shading for backtracking system is correctly calculated\
    In this setup the sun beams should pass beneath the panels with no shading on the preset field. The expected value is 0% ground-shading.

- **Test 40:** Check if self shading for backtracking system is correctly calculated\
    The panels should be positioned horizontally in this setup (to avoid self-shading). Leading to an expected value of 0% self-shading.

## Tests for the sun at the horizon (N)
**Elevation:** 10<sup>-10</sup> °\
**Azimuth:** 0°

### Tracking system
- **Test 41:** Check if ground shading for tracking system is correctly calculated\
    In this setup the sun beams should pass beneath the panels with no shading on the preset field. The expected value is 0% ground-shading.

- **Test 42:** Check if self shading for tracking system is correctly calculated\
    The sun beams should pass between the panels in this system. The expected value is 0% self-shading.

### Vertical system
- **Test 43:** Check if ground shading for vertical system is correctly calculated\
    In this setup the sun beams should pass beneath the panels with no shading on the preset field. The expected value is 0% ground-shading.

- **Test 44:** Check if self shading for vertical system is correctly calculated\
    The sun beams should pass between the panels in this system. The expected value is 0% self-shading.

### Standard system
- **Test 45:** Check if ground shading for standard system is correctly calculated\
    In this setup the sun beams should pass beneath the panels with no shading on the preset field. The expected value is 0% ground-shading.

- **Test 46:** Check if self shading for standard system is correctly calculated\
    With the given panel tilt the sun should eluminate the back of the panels, leading to 100% self-shading by definition.

### Overhead system
- **Test 47:** Check if ground shading for overhead system is correctly calculated\
    In this setup the sun beams should pass beneath the panels with no shading on the preset field. The expected value is 0% ground-shading.

- **Test 48:** Check if self shading for overhead system is correctly calculated\
    The sun beams should pass between the panels in this system. The expected value is 0% self-shading.

### Backtracking system
- **Test 49:** Check if ground shading for backtracking system is correctly calculated\
    In this setup the sun beams should pass beneath the panels with no shading on the preset field. The expected value is 0% ground-shading.

- **Test 50:** Check if self shading for backtracking system is correctly calculated\
    The sun beams should pass between the panels in this system. The expected value is 0% self-shading.

## Tests for half self-shade width
In the following tests the sun is positioned in the east/south and at an elevation that should theoretically produce 50% self-shading on shaded rows.
### Tracking system
**Elevation:** calculated to the value that would theoretically produce half shaded backpanels\
**Azimuth:** 90°

- **Test 51:** Check if self-shading for tracking system is correctly calculated\
    The sun should fully eluminate the first row of panels. All rows behind the first one should be half self-shaded. The expected value is half of the total panel area minus one row in percentage of the total panel area.

### Vertical system
**Elevation:** calculated to the value that would theoretically produce half shaded backpanels\
**Azimuth:** 90°

- **Test 52:** Check if self-shading for vertical system is correctly calculated\
    The sun should fully eluminate the first row of panels. All rows behind the first one should be half self-shaded. The expected value is half of the total panel area minus one row in percentage of the total panel area.

### Standard system
**Elevation:** calculated to the value that would theoretically produce half shaded backpanels\
**Azimuth:** 180°

- **Test 53:** Check if self-shading for standard system is correctly calculated\
    The sun should fully eluminate the first row of panels. All rows behind the first one should be half self-shaded. The expected value is half of the total panel area minus one row in percentage of the total panel area.

### Overhead system
**Elevation:** calculated to the value that would theoretically produce half shaded backpanels\
**Azimuth:** 90°

- **Test 54:** Check if self-shading for overhead system is correctly calculated\
    The sun should fully eluminate the first row of panels. All rows behind the first one should be half self-shaded. The expected value is half of the total panel area minus one row in percentage of the total panel area.

## Tests for half self-shade length
In the following tests the sun is positioned at the horizon and at an azimuth that should theoretically produce 50% self-shading on shaded rows.
### Tracking system
**Elevation:** 10<sup>-10</sup> °\
**Azimuth:** calculated to the value that would theoretically produce half shaded backpanels

- **Test 55:** Check if self-shading for tracking system is correctly calculated\
    The sun should fully eluminate the first row of panels. All rows behind the first one should be half self-shaded. The expected value is half of the total panel area minus one row in percentage of the total panel area.

### Vertical system
**Elevation:** 10<sup>-10</sup> °\
**Azimuth:** calculated to the value that would theoretically produce half shaded backpanels

- **Test 56:** Check if self-shading for vertical system is correctly calculated\
    The sun should fully eluminate the first row of panels. All rows behind the first one should be half self-shaded. The expected value is half of the total panel area minus one row in percentage of the total panel area.

### Standard system
**Elevation:** 10<sup>-10</sup> °\
**Azimuth:** calculated to the value that would theoretically produce half shaded backpanels

- **Test 57:** Check if self-shading for standard system is correctly calculated\
    The sun should fully eluminate the first row of panels. All rows behind the first one should be half self-shaded. The expected value is half of the total panel area minus one row in percentage of the total panel area.

### Overhead system
**Elevation:** 10<sup>-10</sup> °\
**Azimuth:** calculated to the value that would theoretically produce half shaded backpanels

- **Test 58:** Check if self-shading for overhead system is correctly calculated\
    The sun should fully eluminate the first row of panels. All rows behind the first one should be half self-shaded. The expected value is half of the total panel area minus one row in percentage of the total panel area.

## Tests for ground shading at 80° elevation
**Elevation:** 80°

### Tracking system
- **Test 59:** Check if ground shading for tracking system is correctly calculated with the sun at 80° elevation in the east\
    **Azimuth:** 90°\
    The ground-shading should match the seperately calculated expected value, it is the total panel area modified by the sun angle in the E/W plane / the tilt of the PV panel in the E/W plane as a percentage of the total field area.

- **Test 60:** Check if ground shading for tracking system is correctly calculated with the sun at 80° elevation in the west\
    **Azimuth:** 270°\
    The ground-shading should match the seperately calculated expected value, it is the total panel area modified by the sun angle in the E/W plane / the tilt of the PV panel in the E/W plane as a percentage of the total field area.

- **Test 61:** Check if ground shading for tracking system is correctly calculated with the sun at 80° elevation in the south\
    **Azimuth:** 180°\
    The ground-shading should match the seperately calculated expected value, which is the total panel area as a percentage of the total field area.

- **Test 62:** Check if ground shading for tracking system is correctly calculated with the sun at 80° elevation in the north\
    **Azimuth:** 0°\
    The ground-shading should match the seperately calculated expected value, which is the total panel area as a percentage of the total field area.

### Vertical system
- **Test 63:** Check if ground shading for vertical system is correctly calculated with the sun at 80° elevation in the east\
    **Azimuth:** 90°\
    The ground-shading should match the seperately calculated expected value, it is the total panel area modified by the sun angle in the E/W plane / the tilt of the PV panel in the E/W plane as a percentage of the total field area.

- **Test 64:** Check if ground shading for vertical system is correctly calculated with the sun at 80° elevation in the west\
    **Azimuth:** 270°\
    The ground-shading should match the seperately calculated expected value, it is the total panel area modified by the sun angle in the E/W plane / the tilt of the PV panel in the E/W plane as a percentage of the total field area.

- **Test 65:** Check if ground shading for vertical system is correctly calculated with the sun at 80° elevation in the south\
    **Azimuth:** 180°\
    The expected ground-shading value is 0%.

- **Test 66:** Check if ground shading for vertical system is correctly calculated with the sun at 80° elevation in the north\
    **Azimuth:** 0°\
    The expected ground-shading value is 0%.

### Standard system
- **Test 67:** Check if ground shading for standard system is correctly calculated with the sun at 80° elevation in the east\
    **Azimuth:** 90°\
    The ground-shading should match the seperately calculated expected value, which is the total panel area projected on the gound as a percentage of the total field area.

- **Test 68:** Check if ground shading for standard system is correctly calculated with the sun at 80° elevation in the west\
    **Azimuth:** 270°\
    The ground-shading should match the seperately calculated expected value, which is the total panel area projected on the gound as a percentage of the total field area.

- **Test 69:** Check if ground shading for standard system is correctly calculated with the sun at 80° elevation in the south\
    **Azimuth:** 180°\
    The ground-shading should match the seperately calculated expected value, it is the total panel area modified by the sun angle in the N/S plane / the tilt of the PV panel in the N/S plane as a percentage of the total field area.

- **Test 70:** Check if ground shading for standard system is correctly calculated with the sun at 80° elevation in the north\
    **Azimuth:** 0°\
    The ground-shading should match the seperately calculated expected value, it is the total panel area modified by the sun angle in the N/S plane / the tilt of the PV panel in the N/S plane as a percentage of the total field area.

### Overhead system
- **Test 71:** Check if ground shading for overhead system is correctly calculated with the sun at 80° elevation in the east\
    **Azimuth:** 90°\
    The ground-shading should match the seperately calculated expected value, it is the total panel area modified by the sun angle in the E/W plane / the tilt of the PV panel in the E/W plane as a percentage of the total field area.

- **Test 72:** Check if ground shading for overhead system is correctly calculated with the sun at 80° elevation in the west\
    **Azimuth:** 270°\
    The ground-shading should match the seperately calculated expected value, it is the total panel area modified by the sun angle in the E/W plane / the tilt of the PV panel in the E/W plane as a percentage of the total field area.

- **Test 73:** Check if ground shading for overhead system is correctly calculated with the sun at 80° elevation in the south\
    **Azimuth:** 180°\
    The ground-shading should match the seperately calculated expected value, which is the total panel area projected on the gound as a percentage of the total field area.

- **Test 74:** Check if ground shading for overhead system is correctly calculated with the sun at 80° elevation in the north\
    **Azimuth:** 0°\
    The ground-shading should match the seperately calculated expected value, which is the total panel area projected on the gound as a percentage of the total field area.

### Backtracking system
- **Test 75:** Check if ground shading for backtracking system is correctly calculated with the sun at 80° elevation in the east\
    **Azimuth:** 90°\
    The ground-shading should match the seperately calculated expected value, it is the total panel area modified by the sun angle in the E/W plane / the tilt of the PV panel in the E/W plane as a percentage of the total field area.

- **Test 76:** Check if ground shading for backtracking system is correctly calculated with the sun at 80° elevation in the west\
    **Azimuth:** 270°\
    The ground-shading should match the seperately calculated expected value, it is the total panel area modified by the sun angle in the E/W plane / the tilt of the PV panel in the E/W plane as a percentage of the total field area.

- **Test 77:** Check if ground shading for backtracking system is correctly calculated with the sun at 80° elevation in the south\
    **Azimuth:** 180°\
    The ground-shading should match the seperately calculated expected value, which is the total panel area as a percentage of the total field area.

- **Test 78:** Check if ground shading for backtracking system is correctly calculated with the sun at 80° elevation in the north\
    **Azimuth:** 0°\
    The ground-shading should match the seperately calculated expected value, which is the total panel area as a percentage of the total field area.
