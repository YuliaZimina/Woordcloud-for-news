var dateMask = IMask(
  document.getElementById('date-mask'),
  {
    mask: Date,
    min: new Date(1990, 0, 1),
    max: new Date(2020, 0, 1),
    lazy: false
  });