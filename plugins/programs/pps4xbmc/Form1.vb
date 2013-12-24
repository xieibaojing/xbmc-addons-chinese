' pps4xbmc
'=============
' 开源代码，随意修改，原作者不承担因此引起的法律纠纷。robinttt,2009-12-2
' Version 2.0.3 2013-06-22 (cmeng)
' - Disable Timer running in normal mode
' - Wait some time for other application to settle before taking control

Imports VB = Microsoft.VisualBasic
Imports System.Text
'Imports System.Threading
Imports System.Net.Sockets

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
        (ByVal hwnd As IntPtr, _
         ByVal hWndInsertAfter As IntPtr, _
         ByVal x As Integer, ByVal y As Integer, _
         ByVal cx As Integer, ByVal cy As Integer, _
         ByVal wFlags As Integer) As Boolean

    Private Declare Function ShowWindow Lib "user32" (ByVal handle As IntPtr, ByVal nCmdShow As Integer) As Integer
    Private Declare Sub Sleep Lib "kernel32.dll" (ByVal Milliseconds As Integer)

    Private Const SW_SHOWMAXIMIZED As Integer = 3
    Private Const NORMAL As Integer = 1

    Private Const SWP_NOSIZE = &H1
    Private Const SWP_NOMOVE = &H2 'Retains the current position (ignores X and Y parameters).
    Private Const SWP_SHOWWINDOW = &H40
    Private Const HWND_TOPMOST = -1 'Places the window at the top of the Z order

    Private mobjClient As TcpClient
    Private marData(1024) As Byte
    Private mobjText As New StringBuilder()
    Public Delegate Sub DisplayInvoker(ByVal t As String)

    Dim clientSocket As New System.Net.Sockets.TcpClient
    Dim serverStream As NetworkStream

    Dim KCode(11) As String, Url As String, PlayPause As Long, pRate As Integer

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
                If (fHeight / My.Computer.Screen.Bounds.Height > 0.1) And (fWidth / My.Computer.Screen.Bounds.Width > 0.1) Then
                    ShowWindow(Me.Handle, NORMAL)
                    Me.Left = Me.Left + My.Computer.Screen.Bounds.Width / 20
                    Me.Top = Me.Top + My.Computer.Screen.Bounds.Height / 20
                    Me.Width = ((fWidth / My.Computer.Screen.Bounds.Width) - 0.1) * My.Computer.Screen.Bounds.Width
                    Me.Height = ((fHeight / My.Computer.Screen.Bounds.Height) - 0.1) * My.Computer.Screen.Bounds.Height
                    LB.Text = "画面比例：" & Me.Width & " X " & Me.Height
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
                    LB.Text = "画面比例：" & Me.Width & " X " & Me.Height
                    LB.Visible = True
                    Timer2.Enabled = True
                    Me.Refresh()
                Else
                    Me.Top = 0
                    If (Me.Left + My.Computer.Screen.Bounds.Width / 2) >= My.Computer.Screen.Bounds.Width Then
                        Me.Left = My.Computer.Screen.Bounds.Width
                    ElseIf (Me.Left + My.Computer.Screen.Bounds.Width / 2) < 0 Then
                        Me.Left = -My.Computer.Screen.Bounds.Width
                    Else
                        Me.Left = 0
                    End If
                    ShowWindow(Me.Handle, SW_SHOWMAXIMIZED)
                    LB.Text = "画面比例：" & Me.Width & " X " & Me.Height
                    LB.Visible = True
                    Timer2.Enabled = True
                End If

            Case 5 '播放/暂停
                If PlayPause = 0 Then
                    PowerPlayer1.Pause()
                    PlayPause = 1
                    LB.Text = "暂停"
                    LB.Visible = True
                    ShowCursor(True)
                    Timer2.Enabled = True
                ElseIf PlayPause = 1 Then
                    PowerPlayer1.Pause()
                    PlayPause = 0
                    LB.Text = "播放"
                    LB.Visible = True
                    ShowCursor(False)
                    Timer2.Enabled = True
                Else
                    PowerPlayer1.Play()
                    PlayPause = 0
                    LB.Text = "播放"
                    LB.Visible = True
                    ShowCursor(False)
                    Timer2.Enabled = True
                End If
            Case 6 '停止
                PowerPlayer1.Stop()
                LB.Text = "停止"
                LB.Visible = True
                PlayPause = 2
                Timer2.Enabled = True

            Case 7 '上一章节/10
                If PowerPlayer1.GetPlayPosition / PowerPlayer1.GetPlayDuration > 0.02 Then
                    LB.Text = "播放位置跳至：" & Trim(Str(Int(PowerPlayer1.GetPlayPosition - PowerPlayer1.GetPlayDuration * 0.02))) & "秒，总长度：" & Trim(Str(PowerPlayer1.GetPlayDuration)) & "秒"
                    LB.Visible = True
                    Timer2.Enabled = True
                    PowerPlayer1.SetCurrentPosition(PowerPlayer1.GetPlayPosition - PowerPlayer1.GetPlayDuration * 0.02)
                Else
                    PowerPlayer1.SetCurrentPosition(0)
                    LB.Text = "播放位置跳至：0秒，总长度：" & Trim(Str(PowerPlayer1.GetPlayDuration)) & "秒"
                    LB.Visible = True
                    Timer2.Enabled = True
                End If

            Case 8 '下一章节/10
                If (PowerPlayer1.GetPlayDuration - PowerPlayer1.GetPlayPosition / PowerPlayer1.GetPlayDuration) > 0.02 Then
                    LB.Text = "播放位置跳至：" & Trim(Str(Int(PowerPlayer1.GetPlayPosition + PowerPlayer1.GetPlayDuration * 0.02))) & "秒，总长度：" & Trim(Str(PowerPlayer1.GetPlayDuration)) & "秒"
                    LB.Visible = True
                    Timer2.Enabled = True
                    PowerPlayer1.SetCurrentPosition(PowerPlayer1.GetPlayPosition + PowerPlayer1.GetPlayDuration * 0.02)
                End If
            Case 9 'Exit
                Cmd.Visible = False
                LB.Visible = False
                PowerPlayer1.Stop()
                Me.Close()
            Case 10 'About
                PowerPlayer1.AboutBox()
        End Select
    End Sub

    Private Sub Form1_Load(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles MyBase.Load
        Dim Key As StringBuilder
        Dim tmp As String, Keymap_Path As String
        'Url = "pps://ofu6bvoqedndxosw2aqa.pps/我爱你fix.pfv"
        'pps://w462qewqedndxott2aqg7ksehlica.pps/ce879c45f36f0cbef656392a4e3fcb22bbb1520b.pfv

        On Error Resume Next
        Url = Command()
        If Url <> "" Then
            Me.Top = 0
            Me.Left = 0

            ShowCursor(False)
            LB.Visible = False
            PowerPlayer1.src = Url
            PowerPlayer1.Play()
            Cmd.Focus()
            SetWindowPos(Me.Handle, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOMOVE Or SWP_NOSIZE)  '置顶
            ShowWindow(Me.Handle, SW_SHOWMAXIMIZED) ' Also prevent window being move

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
            'mobjClient = New TcpClient("localhost", 8080)
            'mobjClient.GetStream.BeginRead(marData, 0, 1024, AddressOf DoRead, Nothing)
        Else
            End
        End If
    End Sub

    Private Sub Form1_Resize(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles MyBase.Resize
        LB.Left = 0
        LB.Top = Me.Height / 50
        LB.Width = Me.Width
        LB.Height = Me.Height / 20
        Dim fSize As Single = Int(24 * Me.Height / 1080)
        Me.LB.Font = New Font("Arial", fSize, FontStyle.Bold)

        PowerPlayer1.Left = 0
        PowerPlayer1.Top = 0
        PowerPlayer1.Width = Me.Width
        PowerPlayer1.Height = Me.Height
    End Sub

    Private Sub Cmd_KeyDown(sender As Object, e As System.Windows.Forms.KeyEventArgs) Handles Cmd.KeyDown
        Dim i As Long
        ' Remote Control (Some remote player control buttons consumed and taken action by system)
        ' 声音缩小:V- 声音放大:V+ 静音:Vm 画面缩小:↓ 画面放大:↑ 播放暂停:ENT 停止:0 上一章节:← 下一章节:→ 关闭程序:Esc 关于:F1
        Dim remote As Integer() = {174, 175, 173, 40, 38, 13, 0, 37, 39, 27, 112}
        'Cmd.Text = e.KeyCode

        For i = 0 To 10
            If KCode(i) = Trim(Str(e.KeyCode)) & "," & CInt(e.Shift) Then
                SetPosition(i)
                Exit Sub
            ElseIf remote(i) = e.KeyCode Then
                SetPosition(i)
                Exit Sub
            End If
        Next
    End Sub

    Private Sub Cmd_KeyPress(KeyAscii As Integer)
        KeyAscii = 0
    End Sub

    Private Sub Form1_Deactivate(sender As Object, e As EventArgs) Handles Me.Deactivate
        If Cmd.Visible = True Then ' raising form to topmost only if it not in exit mode
            'Wait some time for other application to settle before taking control
            Timer1.Enabled = True
        End If
    End Sub

    Private Sub Timer1_Tick(sender As System.Object, e As System.EventArgs) Handles Timer1.Tick
        Timer1.Enabled = False
        LB.Text = "恢复控制权 ..."
        LB.Visible = True
        Timer2.Enabled = True
    End Sub

    Private Sub Timer2_Tick(sender As System.Object, e As System.EventArgs) Handles Timer2.Tick
        Timer2.Enabled = False
        If LB.Visible = True Then
            LB.Visible = False
            Me.Focus()
            Cmd.Focus()
            SetWindowPos(Me.Handle, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOMOVE Or SWP_NOSIZE)  '置顶
        End If
    End Sub

    ' TCP Client Start

    'Private Sub DisplayText(ByVal t As String)
    '    TextBox_TCP.AppendText(t)
    'End Sub

    'Private Sub DoRead(ByVal ar As IAsyncResult)
    '    Dim intCount As Integer

    '    Try
    '        intCount = mobjClient.GetStream.EndRead(ar)
    '        If intCount < 1 Then
    '            Throw New System.Net.Sockets.SocketException()
    '            Exit Sub
    '        End If

    '        BuildString(marData, 0, intCount)

    '        mobjClient.GetStream.BeginRead(marData, 0, 1024, AddressOf DoRead, Nothing)
    '    Catch e As Exception
    '        'OnDisconnect()
    '    End Try
    'End Sub

    'Private Sub BuildString(ByVal Bytes() As Byte, ByVal offset As Integer, ByVal count As Integer)
    '    Dim intIndex As Integer

    '    For intIndex = offset To offset + count - 1
    '        If Bytes(intIndex) = 10 Then
    '            mobjText.Append(vbLf)

    '            Dim params() As Object = {mobjText.ToString}
    '            Me.Invoke(New DisplayInvoker(AddressOf Me.DisplayText), params)
    '            mobjText = New StringBuilder()
    '        Else
    '            mobjText.Append(ChrW(Bytes(intIndex)))
    '        End If
    '    Next
    'End Sub

    'Private Sub Timer1_Tick(sender As System.Object, e As System.EventArgs) Handles Timer1.Tick
    '    Dim inStream(1024) As Byte
    '    Dim serverStream As NetworkStream = clientSocket.GetStream()
    '    serverStream.Read(inStream, 0, CInt(clientSocket.ReceiveBufferSize))
    '    Dim rxdata As String = System.Text.Encoding.ASCII.GetString(inStream)
    '    If rxdata <> "" Then
    '        TB_TCP.Text = "Data from XBMC: " + rxdata
    '    End If
    'End Sub

    Private Sub PowerPlayer1_PlayStop(sender As System.Object, e As System.EventArgs) Handles PowerPlayer1.PlayStop

    End Sub
End Class


