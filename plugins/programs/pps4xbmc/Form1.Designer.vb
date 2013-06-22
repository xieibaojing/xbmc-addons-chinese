<Global.Microsoft.VisualBasic.CompilerServices.DesignerGenerated()> _
Partial Class frmPPS
    Inherits System.Windows.Forms.Form

    'Form overrides dispose to clean up the component list.
    <System.Diagnostics.DebuggerNonUserCode()> _
    Protected Overrides Sub Dispose(ByVal disposing As Boolean)
        Try
            If disposing AndAlso components IsNot Nothing Then
                components.Dispose()
            End If
        Finally
            MyBase.Dispose(disposing)
        End Try
    End Sub

    'Required by the Windows Form Designer
    Private components As System.ComponentModel.IContainer

    'NOTE: The following procedure is required by the Windows Form Designer
    'It can be modified using the Windows Form Designer.  
    'Do not modify it using the code editor.
    <System.Diagnostics.DebuggerStepThrough()> _
    Private Sub InitializeComponent()
        Me.components = New System.ComponentModel.Container()
        Dim resources As System.ComponentModel.ComponentResourceManager = New System.ComponentModel.ComponentResourceManager(GetType(frmPPS))
        Me.Timer2 = New System.Windows.Forms.Timer(Me.components)
        Me.LB = New System.Windows.Forms.Label()
        Me.Cmd = New System.Windows.Forms.TextBox()
        Me.PowerPlayer1 = New AxPowerPlayerULib.AxPowerPlayerU()
        Me.TextBox_TCP = New System.Windows.Forms.TextBox()
        Me.Timer1 = New System.Windows.Forms.Timer(Me.components)
        CType(Me.PowerPlayer1, System.ComponentModel.ISupportInitialize).BeginInit()
        Me.SuspendLayout()
        '
        'Timer2
        '
        Me.Timer2.Interval = 4000
        '
        'LB
        '
        Me.LB.Anchor = System.Windows.Forms.AnchorStyles.Top
        Me.LB.BackColor = System.Drawing.Color.Black
        Me.LB.Font = New System.Drawing.Font("Microsoft Sans Serif", 18.0!, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, CType(0, Byte))
        Me.LB.ForeColor = System.Drawing.SystemColors.ControlLightLight
        Me.LB.Location = New System.Drawing.Point(33, -1)
        Me.LB.Name = "LB"
        Me.LB.Size = New System.Drawing.Size(556, 29)
        Me.LB.TabIndex = 0
        Me.LB.TextAlign = System.Drawing.ContentAlignment.MiddleCenter
        '
        'Cmd
        '
        Me.Cmd.Font = New System.Drawing.Font("Microsoft Sans Serif", 8.25!, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, CType(0, Byte))
        Me.Cmd.ForeColor = System.Drawing.SystemColors.MenuHighlight
        Me.Cmd.Location = New System.Drawing.Point(2, -1)
        Me.Cmd.Name = "Cmd"
        Me.Cmd.Size = New System.Drawing.Size(25, 20)
        Me.Cmd.TabIndex = 1
        '
        'PowerPlayer1
        '
        Me.PowerPlayer1.Enabled = True
        Me.PowerPlayer1.Location = New System.Drawing.Point(51, 66)
        Me.PowerPlayer1.Name = "PowerPlayer1"
        Me.PowerPlayer1.OcxState = CType(resources.GetObject("PowerPlayer1.OcxState"), System.Windows.Forms.AxHost.State)
        Me.PowerPlayer1.Size = New System.Drawing.Size(510, 178)
        Me.PowerPlayer1.TabIndex = 2
        '
        'TextBox_TCP
        '
        Me.TextBox_TCP.Location = New System.Drawing.Point(595, -1)
        Me.TextBox_TCP.Name = "TextBox_TCP"
        Me.TextBox_TCP.Size = New System.Drawing.Size(30, 20)
        Me.TextBox_TCP.TabIndex = 3
        Me.TextBox_TCP.Visible = False
        '
        'Timer1
        '
        Me.Timer1.Interval = 7000
        '
        'frmPPS
        '
        Me.AutoScaleDimensions = New System.Drawing.SizeF(6.0!, 13.0!)
        Me.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
        Me.BackColor = System.Drawing.SystemColors.GradientActiveCaption
        Me.ClientSize = New System.Drawing.Size(624, 315)
        Me.Controls.Add(Me.LB)
        Me.Controls.Add(Me.PowerPlayer1)
        Me.Controls.Add(Me.TextBox_TCP)
        Me.Controls.Add(Me.Cmd)
        Me.FormBorderStyle = System.Windows.Forms.FormBorderStyle.None
        Me.Name = "frmPPS"
        Me.Text = "Form1"
        Me.TopMost = True
        CType(Me.PowerPlayer1, System.ComponentModel.ISupportInitialize).EndInit()
        Me.ResumeLayout(False)
        Me.PerformLayout()

    End Sub
    Friend WithEvents Timer2 As System.Windows.Forms.Timer
    Friend WithEvents LB As System.Windows.Forms.Label
    Friend WithEvents Cmd As System.Windows.Forms.TextBox
    Friend WithEvents PowerPlayer1 As AxPowerPlayerULib.AxPowerPlayerU
    Friend WithEvents TextBox_TCP As System.Windows.Forms.TextBox
    Friend WithEvents Timer1 As System.Windows.Forms.Timer

End Class
