{{- define "webnotes.name" -}}
webnotes
{{- end }}

{{- define "webnotes.fullname" -}}
webnotes
{{- end }}

{{- define "mongodb.name" -}}
webnotes-mongo
{{- end }}

{{- define "mongodb.fullname" -}}
webnotes-mongo
{{- end }}

{{- define "webnotes.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "webnotes.labels" -}}
chart: {{ include "webnotes.chart" . }}
{{ include "webnotes.selectorLabels" . }}
{{- if .Chart.AppVersion }}
version: {{ .Chart.AppVersion | quote }}
{{- end }}
{{- end }}

{{- define "webnotes.selectorLabels" -}}
name: {{ include "webnotes.name" . }}
{{- end }}

{{- define "mongodb.chart" -}}
{{- printf "%s-mongo-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "mongodb.labels" -}}
chart: {{ include "mongodb.chart" . }}
{{ include "mongodb.selectorLabels" . }}
{{- if .Chart.AppVersion }}
version: {{ .Chart.AppVersion | quote }}
{{- end }}
{{- end }}

{{- define "mongodb.selectorLabels" -}}
name: {{ include "mongodb.name" . }}
{{- end }}
