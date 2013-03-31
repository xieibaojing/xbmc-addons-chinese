' pps4xbmc
'=============
' 开源代码，随意修改，原作者不承担因此引起的法律纠纷。 robinttt,2009-12-2
' Version 2.0.0 2013-03-30 (cmeng)
' Ported pps4xbmc to VB 2010
' Set PPS player focus to accept user input by default
' Change Fast FWD/PREV to smaller step 0.1 > 0.025
' Auto unmute when changing audio volume level


Imports VB = Microsoft.VisualBasic
Imports System.Text

Public Class frmPPS
    Private Declare Function GetPrivateProfileString Lib "kernel32" Alias "GetPrivateProfileStringA" _
        (ByVal lpApplicationName As String, _
         ByVal lpKeyName As String, _
         ByVal lpDefault As String, _
         ByVal lpReturnedString As StringBuilder, _
         ByVal nSize As Integer, _
         ByVal lpFileName As String) As Integer
    Private Declare Function WritePrivateProfileString Lib "kernel32" Alias "WritePrivateProfileStringA" _
        (ByVal lpApplicationName As String, _
         ByVal lpKeyName As String, _
         ByVal lpString As String, _
         ByVal lpFileName As String) As Boolean
    Private Declare Function ShowCursor Lib "user32" (ByVal bShow As Boolean) As Integer
    Private Declare Function SetWindowPos Lib "user32" _
        (ByVal hwnd As Long, _
         ByVal hWndInsertAfter As Long, _
         ByVal x As Long, ByVal y As Long, _
         ByVal cx As Long, ByVal cy As Long, _
         ByVal wFlags As Long) As Long
    Private Declare Function ShowWindow Lib "user32" (ByVal hwnd As Long, ByVal nCmdShow As Long) As Long

    Private Const SWP_NOSIZE = &H1
    Private Const SWP_NOMOVE = &H2
    Private Const SWP_SHOWWINDOW = &H40
    Private Const HWND_TOPMOST = -1

    Dim KCode(10) As String, Url As String, PlayPause As Long


    Private Sub SetPosition(Code As Long)
        On Error Resume Next
        Dim fWidth As Long, fHeight As Long, V As Long
        fWidth = Me.Width
        fHeight = Me.Height

        Select Case Code
            Case 0 '声音缩小
                V = PowerPlayer1.Volume
                PowerPlayer1.Mute = False
                If V - 10 < 0 Then
                    PowerPlayer1.Volume = 0
                    LB.Text = "音量：0%"
                    LB.Visible = True
                    Timer2.Enabled = True
                Else
                    PowerPlayer1.Volume = V - 10
                    LB.Text = "音量：" & Trim(Str(V - 10)) & "%"
                    LB.Visible = True
                    Timer2.Enabled = True
                End If

            Case 1 '声音放大
                V = PowerPlayer1.Volume
                PowerPlayer1.Mute = False
                If V + 10 > 100 Then
                    PowerPlayer1.Volume = 100
                    LB.Text = "音量：100%"
                    LB.Visible = True
                    Timer2.Enabled = True
                Else
                    PowerPlayer1.Volume = V + 10
                    LB.Text = "音量：" & Trim(Str(V + 10)) & "%"
                    LB.Visible = True
                    Timer2.Enabled = True
                End If

            Case 2 '静音
                If PowerPlayer1.Mute = True Then
                    PowerPlayer1.Mute = False
                    LB.Text = "取消静音"
                    LB.Visible = True
                    Timer2.Enabled = True
                Else
                    PowerPlayer1.Mute = True
                    LB.Text = "静音"
                    LB.Visible = True
                    Timer2.Enabled = True
                End If

            Case 3 '画面缩小
                If fWidth / My.Computer.Screen.Bounds.Width > 0.1 Then
                    Me.Left = Me.Left + My.Computer.Screen.Bounds.Width / 20
                    Me.Top = Me.Top + My.Computer.Screen.Bounds.Height / 20
                    Me.Width = ((fWidth / My.Computer.Screen.Bounds.Width) - 0.1) * My.Computer.Screen.Bounds.Width
                    Me.Height = ((fHeight / My.Computer.Screen.Bounds.Height) - 0.1) * My.Computer.Screen.Bounds.Height
                    LB.Text = "画面比例：" & Int(Me.Width / 15) & " X " & Int(Me.Height / 15)
                    LB.Visible = True
                    Timer2.Enabled = True
                    Me.Refresh()
                End If

            Case 4 '画面放大
                If fWidth < My.Computer.Screen.Bounds.Width Then
                    Me.Left = Me.Left - My.Computer.Screen.Bounds.Width / 20
                    Me.Top = Me.Top - My.Computer.Screen.Bounds.Height / 20
                    Me.Width = ((fWidth / My.Computer.Screen.Bounds.Width) + 0.1) * My.Computer.Screen.Bounds.Width
                    Me.Height = ((fHeight / My.Computer.Screen.Bounds.Height) + 0.1) * My.Computer.Screen.Bounds.Height
                    LB.Text = "画面比例：" & Int(Me.Width / 15) & " X " & Int(Me.Height / 15)
                    LB.Visible = True
                    Timer2.Enabled = True
                    Me.Refresh()
                End If

            Case 5 '播放/暂停
                If PlayPause = 0 Then
                    PowerPlayer1.Pause()
                    PlayPause = 1
                    LB.Text = "暂停"
                    LB.Visible = True
                    Timer2.Enabled = True
                ElseIf PlayPause = 1 Then
                    PowerPlayer1.Pause()
                    PlayPause = 0
                    LB.Text = "播放"
                    LB.Visible = True
                    Timer2.Enabled = True
                Else
                    PowerPlayer1.Play()
                    PlayPause = 0
                    LB.Text = "播放"
                    LB.Visible = True
                    Timer2.Enabled = True
                End If
            Case 6 '停止
                PowerPlayer1.Stop()
                LB.Text = "停止"
                LB.Visible = True
                PlayPause = 2
                Timer2.Enabled = True

            Case 7 '上一章节/10
                If PowerPlayer1.GetPlayPosition / PowerPlayer1.GetPlayDuration > 0.025 Then
                    LB.Text = "播放位置跳至：" & Trim(Str(PowerPlayer1.GetPlayPosition - PowerPlayer1.GetPlayDuration * 0.025)) & "秒，总长度：" & Trim(Str(PowerPlayer1.GetPlayDuration)) & "秒"
                    LB.Visible = True
                    Timer2.Enabled = True
                    PowerPlayer1.SetCurrentPosition(PowerPlayer1.GetPlayPosition - PowerPlayer1.GetPlayDuration * 0.025)
                Else
                    PowerPlayer1.SetCurrentPosition(0)
                    LB.Text = "播放位置跳至：0秒，总长度：" & Trim(Str(PowerPlayer1.GetPlayDuration)) & "秒"
                    LB.Visible = True
                    Timer2.Enabled = True
                End If

            Case 8 '下一章节/10
                If (PowerPlayer1.GetPlayDuration - PowerPlayer1.GetPlayPosition / PowerPlayer1.GetPlayDuration) > 0.025 Then
                    LB.Text = "播放位置跳至：" & Trim(Str(PowerPlayer1.GetPlayPosition + PowerPlayer1.GetPlayDuration * 0.025)) & "秒，总长度：" & Trim(Str(PowerPlayer1.GetPlayDuration)) & "秒"
                    LB.Visible = True
                    Timer2.Enabled = True
                    PowerPlayer1.SetCurrentPosition(PowerPlayer1.GetPlayPosition + PowerPlayer1.GetPlayDuration * 0.025)
                End If
            Case 9
                PowerPlayer1.Stop()
                Me.Close()
        End Select
    End Sub

    Private Sub Form1_Load(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles MyBase.Load
        Dim Key As StringBuilder
        Dim tmp As String, Keymap_Path As String

        On Error Resume Next
        'Url = "pps://ofu6bvoqedndxosw2aqa.pps/我爱你fix.pfv"
        Url = Command()
        If Url <> "" Then
            Me.Top = 0
            Me.Left = 0
            Me.Width = My.Computer.Screen.Bounds.Width 'Screen.PrimaryScreen.Bounds.Width 
            Me.Height = My.Computer.Screen.Bounds.Height 'Screen.PrimaryScreen.Bounds.Height

            PowerPlayer1.src = Url
            PowerPlayer1.Play()
            Me.Show()
            ShowCursor(False)
            LB.Visible = False
            Cmd.Focus()
            'SetWindowPos(PowerPlayer1.Handle, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOMOVE Or SWP_NOSIZE)  '置顶

            Keymap_Path = Application.StartupPath & "\KeyMap.ini"
            If Dir(Keymap_Path) = "" Then    '写配置文件
                MsgBox("未发现配置文件，请先运行KeymapSet设置快捷键")
            Else '读配置文件
                Key = New StringBuilder(255)
                tmp = GetPrivateProfileString("声音缩小", "Keycode", "", Key, Key.Capacity, Keymap_Path)
                KCode(0) = Key.ToString
                tmp = GetPrivateProfileString("声音放大", "Keycode", "", Key, Key.Capacity, Keymap_Path)
                KCode(1) = Key.ToString
                tmp = GetPrivateProfileString("静    音", "Keycode", "", Key, Key.Capacity, Keymap_Path)
                KCode(2) = Key.ToString
                tmp = GetPrivateProfileString("画面缩小", "Keycode", "", Key, Key.Capacity, Keymap_Path)
                KCode(3) = Key.ToString
                tmp = GetPrivateProfileString("画面放大", "Keycode", "", Key, Key.Capacity, Keymap_Path)
                KCode(4) = Key.ToString
                tmp = GetPrivateProfileString("播放暂停", "Keycode", "", Key, Key.Capacity, Keymap_Path)
                KCode(5) = Key.ToString
                tmp = GetPrivateProfileString("停    止", "Keycode", "", Key, Key.Capacity, Keymap_Path)
                KCode(6) = Key.ToString
                tmp = GetPrivateProfileString("上一章节", "Keycode", "", Key, Key.Capacity, Keymap_Path)
                KCode(7) = Key.ToString
                tmp = GetPrivateProfileString("下一章节", "Keycode", "", Key, Key.Capacity, Keymap_Path)
                KCode(8) = Key.ToString
                tmp = GetPrivateProfileString("关闭程序", "Keycode", "", Key, Key.Capacity, Keymap_Path)
                KCode(9) = Key.ToString
            End If
        Else
            End
        End If
    End Sub

    Private Sub Form1_Resize(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles MyBase.Resize
        LB.Left = 0
        LB.Top = Me.Height * 120 / 7170
        LB.Width = Me.Width
        LB.Height = Me.Height * 375 / 7170
        Dim fSize As Single = Int(24 * Me.Height / 1080)
        Me.LB.Font = New Font("Arial", fSize, FontStyle.Bold)

        PowerPlayer1.Left = 0
        PowerPlayer1.Top = 0
        PowerPlayer1.Width = Me.Width
        PowerPlayer1.Height = Me.Height
    End Sub

    Private Sub Cmd_KeyDown(sender As Object, e As System.Windows.Forms.KeyEventArgs) Handles Cmd.KeyDown
        Dim i As Long
        For i = 0 To 9
            If KCode(i) = Trim(Str(e.KeyCode)) & "," & CInt(e.Shift) Then
                SetPosition(i)
                Exit Sub
            End If
        Next
    End Sub

    Private Sub Cmd_KeyPress(KeyAscii As Integer)
        KeyAscii = 0
    End Sub

    Private Sub Timer2_Tick(sender As System.Object, e As System.EventArgs) Handles Timer2.Tick
        If LB.Visible = True Then
            LB.Visible = False
        End If
    End Sub

End Class


