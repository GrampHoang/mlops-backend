oc get template
oc new-app <template-name>

oc edit template <tempate-name>


oc create secret docker-registry artifactory \
--docker-server=https://artifactorymlopsk18.jfrog.io \
--docker-username=jenkins \
--docker-password=Hello@1234@@ \
--docker-email=chiengphihoang.008219@gmail.com