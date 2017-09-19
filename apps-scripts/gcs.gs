var params = {
    CLIENT_ID: 'client-id',
    CLIENT_SECRET: 'secret',
    BUCKET_NAME: 'gcs-bucket-name',
};

function uploadFileToGCS(filename, data) {

    var service = getService();
    if (!service.hasAccess()) {
        Logger.log("Please authorize %s", service.getAuthorizationUrl());
        return;
    }

    var bytes = Utilities.newBlob(data, "application/json; charset=utf-8").getBytes();

    var url = 'https://www.googleapis.com/upload/storage/v1/b/BUCKET/o?uploadType=media&name=FILE'
        .replace("BUCKET", params.BUCKET_NAME)
        .replace("FILE", encodeURIComponent(filename));

    var response = UrlFetchApp.fetch(url, {
        method: "POST",
        contentLength: bytes.length,
        contentType: "application/json; charset=utf-8",
        payload: bytes,
        headers: {
            Authorization: 'Bearer ' + service.getAccessToken()
        }
    });

    var result = JSON.parse(response.getContentText());
    Logger.log(JSON.stringify(result, null, 2));
}

function getService() {
    return OAuth2.createService('gcs')
        .setAuthorizationBaseUrl('https://accounts.google.com/o/oauth2/auth')
        .setTokenUrl('https://accounts.google.com/o/oauth2/token')
        .setClientId(params.CLIENT_ID)
        .setClientSecret(params.CLIENT_SECRET)
        .setCallbackFunction('authCallback')
        .setPropertyStore(PropertiesService.getUserProperties())
        .setScope('https://www.googleapis.com/auth/devstorage.read_write')
        .setParam('access_type', 'offline')
        .setParam('approval_prompt', 'force')
        .setParam('login_hint', Session.getActiveUser().getEmail());
}

function authCallback(request) {
    var service = getService();
    var authorized = service.handleCallback(request);
    if (authorized) {
        return HtmlService.createHtmlOutput('Connected to Google Cloud Storage');
    } else {
        return HtmlService.createHtmlOutput('Access Denied');
    }
}
