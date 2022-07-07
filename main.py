import eel
import wx
import librosa
import numpy as np
import soundfile as sf

@eel.expose
def getFolder(wildcard="*"):
    
    app = wx.App(None)
    style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
    dialog = wx.FileDialog(None, 'Open', wildcard=wildcard, style=style)
    if dialog.ShowModal() == wx.ID_OK:
        path = dialog.GetPath()
    else:
        path = None
    dialog.Destroy()
    return path

@eel.expose
def pitchShift(filename, num_steps):
    print("running convert")
    file_name, extension = filename.split(".")
    try: 
        y, sr = librosa.load(filename)
        print("loading finished")
    except RuntimeError:
        return "load_error"
        
    y_new = librosa.effects.pitch_shift(y, sr=sr, n_steps=4)
    print("done shift.")
    print("saving...")
    sf.write(f"{file_name}_shifted_{num_steps}.{extension}", y_new, sr)
    print("done saving.")
    print("running finished!")
    return "success"

eel.init('web')
eel.start('index.html', size=(500, 300))