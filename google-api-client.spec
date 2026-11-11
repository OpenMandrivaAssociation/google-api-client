Name:		google-api-client
Version:	1.34.0
Release:	1
Summary:	Google API Client Library for Java
Group:		Development/Java
License:	Apache-2.0
URL:		https://github.com/googleapis/google-api-java-client
# Tag v1.34.0. The archive has no prebuilt jars or class files.
# Gradle 9.9.1 strictly pins 1.34.0.
Source0:	https://github.com/googleapis/google-api-java-client/archive/refs/tags/v%{version}.tar.gz#/google-api-client-%{version}.tar.gz

BuildArch:	noarch
BuildRequires:	java-current-devel
BuildRequires:	sysjar
BuildRequires:	javapackages-filesystem
BuildRequires:	mvn(com.google.http-client:google-http-client) = 1.42.2
BuildRequires:	mvn(com.google.http-client:google-http-client-gson) = 1.42.2
BuildRequires:	mvn(com.google.http-client:google-http-client-apache-v2) = 1.42.2
BuildRequires:	mvn(com.google.oauth-client:google-oauth-client) = 1.34.1
BuildRequires:	mvn(com.google.guava:guava) = 33.6.0-jre
BuildRequires:	mvn(com.google.guava:failureaccess) = 1.0.3
BuildRequires:	mvn(com.google.code.gson:gson) = 2.14.0
BuildRequires:	mvn(org.apache.httpcomponents:httpclient) = 4.5.14
BuildRequires:	mvn(org.apache.httpcomponents:httpcore) = 4.4.16
BuildRequires:	mvn(commons-logging:commons-logging) = 1.4.0
Requires:	mvn(com.google.http-client:google-http-client) = 1.42.2
Requires:	mvn(com.google.http-client:google-http-client-gson) = 1.42.2
Requires:	mvn(com.google.http-client:google-http-client-apache-v2) = 1.42.2
Requires:	mvn(com.google.oauth-client:google-oauth-client) = 1.34.1
Requires:	mvn(com.google.guava:guava) = 33.6.0-jre
Requires:	mvn(com.google.code.gson:gson) = 2.14.0
Requires:	mvn(org.apache.httpcomponents:httpclient) = 4.5.14
Requires:	mvn(org.apache.httpcomponents:httpcore) = 4.4.16

%description
Google API Client %{version}. Compiled from source against the system
Google HTTP client 1.42.2 and OAuth client 1.34.1. The Apache HttpClient
v1 transport is not compiled: google-http-client 1.42.2 ships only the
v2 transport. Servlet and App Engine modules are not built.

%prep
%autosetup -n google-api-java-client-%{version}
find . \( -name '*.jar' -o -name '*.class' -o -name '*.so' -o -name '*.node' -o -name '*.wasm' \) -delete
sed -i 's/${project.version}/%{version}/' google-api-client/src/main/properties/com/google/api/client/googleapis/google-api-client.properties
grep -F -q 'google-api-client.version=%{version}' google-api-client/src/main/properties/com/google/api/client/googleapis/google-api-client.properties

%build
set -eo pipefail
# googleapis/apache/GoogleApacheHttpTransport.java imports the v1
# ApacheHttpTransport class, which 1.42.2 does not ship. Keep the v2 class.
find google-api-client/src/main/java -name '*.java' \
	! -path '*/googleapis/apache/GoogleApacheHttpTransport.java' > sources.list
test "$(wc -l < sources.list)" -eq 87
if grep -F -q '/googleapis/apache/GoogleApacheHttpTransport.java' sources.list; then
	echo 'v1 Apache transport was not excluded'
	exit 1
fi
grep -F -q '/googleapis/apache/v2/GoogleApacheHttpTransport.java' sources.list
CP=%{_javadir}/google-http-client.jar:%{_javadir}/google-http-client-gson.jar:%{_javadir}/google-http-client-apache-v2.jar:%{_javadir}/google-oauth-client.jar:%{_javadir}/guava.jar:%{_javadir}/failureaccess.jar:%{_javadir}/gson-2.14.0.jar:%{_javadir}/httpcomponents/httpclient.jar:%{_javadir}/httpcomponents/httpcore.jar:%{_javadir}/commons-logging.jar
mkdir -p classes
javac --release 11 -encoding UTF-8 -Xlint:-options -cp "$CP" -d classes @sources.list
mkdir -p classes/com/google/api/client/googleapis
/bin/cp -f google-api-client/src/main/properties/com/google/api/client/googleapis/google-api-client.properties classes/com/google/api/client/googleapis/
/bin/cp -f google-api-client/src/main/resources/com/google/api/client/googleapis/google.p12 classes/com/google/api/client/googleapis/
/bin/cp -f google-api-client/src/main/resources/com/google/api/client/googleapis/google.jks classes/com/google/api/client/googleapis/
cat > manifest.mf << 'EOF'
Manifest-Version: 1.0
Automatic-Module-Name: com.google.api.client.googleapis

EOF
jar cfm google-api-client.jar manifest.mf -C classes .
jar i google-api-client.jar
javap -verbose -cp google-api-client.jar com.google.api.client.googleapis.GoogleUtils | grep -F 'major version: 55'

cat > google-api-client.pom << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.google.api-client</groupId>
  <artifactId>google-api-client</artifactId>
  <version>1.34.0</version>
  <name>Google API Client</name>
  <description>Google API Client Library for Java</description>
  <licenses>
    <license>
      <name>Apache-2.0</name>
    </license>
  </licenses>
  <dependencies>
    <dependency>
      <groupId>com.google.http-client</groupId>
      <artifactId>google-http-client</artifactId>
      <version>1.42.2</version>
    </dependency>
    <dependency>
      <groupId>com.google.http-client</groupId>
      <artifactId>google-http-client-gson</artifactId>
      <version>1.42.2</version>
    </dependency>
    <dependency>
      <groupId>com.google.http-client</groupId>
      <artifactId>google-http-client-apache-v2</artifactId>
      <version>1.42.2</version>
    </dependency>
    <dependency>
      <groupId>com.google.oauth-client</groupId>
      <artifactId>google-oauth-client</artifactId>
      <version>1.34.1</version>
    </dependency>
    <dependency>
      <groupId>com.google.guava</groupId>
      <artifactId>guava</artifactId>
      <version>33.6.0-jre</version>
    </dependency>
    <dependency>
      <groupId>com.google.code.gson</groupId>
      <artifactId>gson</artifactId>
      <version>2.14.0</version>
    </dependency>
    <dependency>
      <groupId>org.apache.httpcomponents</groupId>
      <artifactId>httpclient</artifactId>
      <version>4.5.14</version>
    </dependency>
    <dependency>
      <groupId>org.apache.httpcomponents</groupId>
      <artifactId>httpcore</artifactId>
      <version>4.4.16</version>
    </dependency>
  </dependencies>
</project>
EOF

%install
sysjar install --buildroot %{buildroot} \
	--artifact google-api-client.pom:google-api-client.jar \
	--file-name google-api-client \
	--filelist .mfiles

%check
set -eo pipefail
JAR=%{buildroot}%{_javadir}/google-api-client.jar
test -f "$JAR"
mkdir -p check
cat > check/Smoke.java << 'EOF'
import com.google.api.client.googleapis.GoogleUtils;
import java.security.KeyStore;
public class Smoke {
	public static void main(String[] args) throws Exception {
		KeyStore ks = GoogleUtils.getCertificateTrustStore();
		String version = GoogleUtils.VERSION;
		if (!"PKCS12".equals(ks.getType()) || ks.size() != 70 || !"1.34.0".equals(version)) {
			throw new RuntimeException(ks.getType() + " " + ks.size() + " " + version);
		}
		System.out.println("gapi_ok " + ks.getType() + " " + ks.size() + " " + version);
	}
}
EOF
CP="$JAR:%{_javadir}/google-http-client.jar:%{_javadir}/google-http-client-gson.jar:%{_javadir}/google-http-client-apache-v2.jar:%{_javadir}/google-oauth-client.jar:%{_javadir}/guava.jar:%{_javadir}/failureaccess.jar:%{_javadir}/gson-2.14.0.jar:%{_javadir}/httpcomponents/httpclient.jar:%{_javadir}/httpcomponents/httpcore.jar:%{_javadir}/commons-logging.jar"
javac --release 11 -encoding UTF-8 -Xlint:-options -cp "$CP" -d check check/Smoke.java
java -cp "check:$CP" Smoke > check/out.txt
cat check/out.txt
grep -F -q 'gapi_ok PKCS12 70 1.34.0' check/out.txt

%files -f .mfiles
%doc LICENSE README.md
