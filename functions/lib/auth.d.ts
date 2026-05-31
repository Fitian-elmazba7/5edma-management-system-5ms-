import * as functions from 'firebase-functions';
export declare const setUserRole: functions.HttpsFunction & functions.Runnable<any>;
export declare const onUserCreate: functions.CloudFunction<import("firebase-admin/lib/auth").UserRecord>;
