from merida.lightcurves_cls import LightCurvesNExSciLocalFeather
from merida.zones_for_lightcurves import plotter
from bokeh.io import save, output_file, export_png
from bokeh.models import Range1d

def main(lightcurve_name_, lightcurve_class_, data_path_):
    the_lightcurve = LightCurvesNExSciLocalFeather(lightcurve_name_=lightcurve_name_,
                                                               lightcurve_class_=lightcurve_class_,
                                                               data_path_=data_path_)
    days, fluxes, cor_fluxes, fluxes_errors = the_lightcurve.get_days_fluxes_errors()
    # three_starting_and_ending_days = three_highest_intervals_finder(days, fluxes)

    plot, widget_inputs = plotter(the_lightcurve, height_and_width_=(325, 900), high_mag_plotting_=False,
                                  starting_and_ending_days_1_=None,
                                  starting_and_ending_days_2_=None, starting_and_ending_days_3_=None)
    plot.xaxis.axis_label = 'Days'
    plot.yaxis.axis_label = 'Flux'
    plot.x_range = Range1d(3824, 4040)
    plot.y_range = Range1d(-20000, 70000)
    output_file(f"{lightcurve_name_}.html")
    save(plot)
    # export_png(plot, filename=f"{lightcurve_name_}.png")

if __name__ == '__main__':
    lightcurve_name = 'gb9-R-8-5-27219'
    lightcurve_class = 'negative'
    data_local = True
    # internal:
    general_path = '/Users/stela/Documents/Scripts/ai_microlensing/qusi_microlensing/data/microlensing_2M'
    data_folder = f'{general_path}/{lightcurve_name.split("-")[0]}/'
    main(lightcurve_name, lightcurve_class, data_folder)