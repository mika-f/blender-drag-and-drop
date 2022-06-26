// ------------------------------------------------------------------------------------------
//  Copyright (c) Natsuneko. All rights reserved.
//  Licensed under the MIT License. See LICENSE in the project root for license information.
// ------------------------------------------------------------------------------------------

using System;
using System.Diagnostics;
using System.IO;
using System.Runtime.InteropServices;
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
        CreateShortcutButton.IsEnabled = false;
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
            LaunchButton.IsEnabled = false;
            CreateShortcutButton.IsEnabled = false;
            return;
        }

        BlenderLocation.Text = file;
        LaunchButton.IsEnabled = true;
        CreateShortcutButton.IsEnabled = true;
    }

    private void OnClickCreateShortcutButton(object sender, RoutedEventArgs e)
    {
        var dialog = new SaveFileDialog
        {
            FileName = "Blender.lnk",
            CheckPathExists = true,
            Filter = "Shortcut File (*.lnk)|*.lnk"
        };

        if (dialog.ShowDialog() == false)
            return;

        var file = dialog.FileName;
        var t = Type.GetTypeFromCLSID(new Guid("72C24DD5-D70A-438B-8A42-98424B88AFB8"));
        if (t == null)
            return;

        dynamic? shell = Activator.CreateInstance(t);
        if (shell == null)
            return;

        var shortcut = shell.CreateShortcut(file);
        if (shortcut == null)
            return;

        var executable = Path.GetFullPath("./blender-launcher.exe");
        shortcut.TargetPath = $"\"{executable}\"";
        shortcut.Arguments = $"\"{BlenderLocation.Text}\"";
        shortcut.IconLocation = $"{BlenderLocation.Text},0";
        shortcut.Save();

        Marshal.FinalReleaseComObject(shortcut);
        Marshal.FinalReleaseComObject(shell);
    }
}