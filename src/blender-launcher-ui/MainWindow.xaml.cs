// ------------------------------------------------------------------------------------------
//  Copyright (c) Natsuneko. All rights reserved.
//  Licensed under the MIT License. See LICENSE in the project root for license information.
// ------------------------------------------------------------------------------------------

using System.Diagnostics;
using System.IO;
using System.Windows;

using Microsoft.Win32;

namespace NatsunekoLaboratory.BlenderLauncher.UI;

/// <summary>
///     Interaction logic for MainWindow.xaml
/// </summary>
public partial class MainWindow : Window
{
    public MainWindow()
    {
        InitializeComponent();
        LaunchButton.IsEnabled = false;
    }

    private void OnClickLaunchButton(object sender, RoutedEventArgs e)
    {
        var path = "./blender-launcher.exe";
        if (File.Exists(path))
            Process.Start("./blender-launcher.exe", new[] { BlenderLocation.Text });
        else
            MessageBox.Show($"File Not Found: {path}");
    }

    private void OnClickOpenFileButton(object sender, RoutedEventArgs e)
    {
        var dialog = new OpenFileDialog
        {
            Filter = "Blender Executable (*.exe)|*.exe"
        };

        if (dialog.ShowDialog() == false)
            return;

        var file = dialog.FileName;
        if (!file.ToLowerInvariant().EndsWith("blender.exe"))
        {
            MessageBox.Show("Please select blender.exe");
            return;
        }

        BlenderLocation.Text = file;
        LaunchButton.IsEnabled = true;
    }
}