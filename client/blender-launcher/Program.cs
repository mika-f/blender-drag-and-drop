// ------------------------------------------------------------------------------------------
//  Copyright (c) Natsuneko. All rights reserved.
//  Licensed under the MIT License. See LICENSE in the project root for license information.
// ------------------------------------------------------------------------------------------

using System.Diagnostics;

if (args.Length != 2)
    return 1;

var executable = args[0];
var injector = args[1];
var process = new Process
{
    EnableRaisingEvents = true,
    StartInfo =
    {
        FileName = executable,
        CreateNoWindow = true,
        RedirectStandardError = true,
        RedirectStandardOutput = true,
        UseShellExecute = false
    }
};

if (!process.Start())
    return 1;

var processId = process.Id;
Process.Start(injector, processId.ToString());

process.OutputDataReceived += (sender, e) => Console.WriteLine(e.Data);
process.ErrorDataReceived += (sender, e) => Console.WriteLine(e.Data);

process.BeginOutputReadLine();
process.BeginErrorReadLine();
process.WaitForExit();

return 0;