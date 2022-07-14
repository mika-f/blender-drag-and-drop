// ------------------------------------------------------------------------------------------
//  Copyright (c) Natsuneko. All rights reserved.
//  Licensed under the MIT License. See LICENSE in the project root for license information.
// ------------------------------------------------------------------------------------------

using System.Diagnostics;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;

if (args.Length != 1)
    return 1;

var executable = args[0];
var self = Path.GetFullPath(AppContext.BaseDirectory);
var process = new Process
{
    EnableRaisingEvents = true,
    StartInfo =
    {
        FileName = executable,
        Arguments = $"--python {Path.GetFullPath(Path.Combine(self, "blender-server", "launch.py"))}",
        CreateNoWindow = true,
        RedirectStandardError = true,
        RedirectStandardOutput = true,
        StandardOutputEncoding = Encoding.UTF8,
        UseShellExecute = false
    }
};

if (!process.Start())
    return 1;

var processId = process.Id;
var startInfo = new ProcessStartInfo
{
    FileName = Path.Combine(self, "blender-hook.exe"),
    Arguments = processId.ToString(),
    CreateNoWindow = true,
    UseShellExecute = false,
    WorkingDirectory = self
};
Process.Start(startInfo)!.WaitForExit();

var client = new HttpClient();

process.OutputDataReceived += async (sender, e) =>
{
    var str = e.Data;
    if (string.IsNullOrWhiteSpace(str))
        return;


    if (!str.StartsWith("f:"))
    {
        Console.WriteLine(str);
        return;
    }

    try
    {
        var path = str["f:".Length..].Trim();
        if (!File.Exists(path))
        {
            Console.WriteLine($"[blender-launcher] invalid file path detected: {path}");
            return;
        }

        Console.WriteLine($"[blender-launcher] start to send {path} to blender server");

        var json = JsonSerializer.Serialize(new ImportRequest { Path = path });
        var content = new StringContent(json, Encoding.UTF8, "application/json");
        await client.PostAsync("http://localhost:7225/", content);
    }
    catch
    {
        // ignored
    }
};
process.ErrorDataReceived += (sender, e) => Console.WriteLine(e.Data);

process.BeginOutputReadLine();
process.BeginErrorReadLine();
process.WaitForExit();

return 0;

internal class ImportRequest
{
    [JsonPropertyName("path")]
    public string Path { get; set; }
}