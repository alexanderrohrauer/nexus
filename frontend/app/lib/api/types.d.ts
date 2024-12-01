/**
 * This file was auto-generated by openapi-typescript.
 * Do not make direct changes to the file.
 */

export interface paths {
    "/": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Root */
        get: operations["root__get"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
}
export type webhooks = Record<string, never>;
export interface components {
    schemas: {
        /** Category */
        Category: {
            /** Name */
            name: string;
            /** Description */
            description: string;
        };
        /** HTTPValidationError */
        HTTPValidationError: {
            /** Detail */
            detail?: components["schemas"]["ValidationError"][];
        };
        /** Product */
        Product: {
            /**
             *  Id
             * @description MongoDB document ObjectID
             */
            _id?: string | null;
            /** Name */
            name: string;
            /** Description */
            description: string | null;
            /** Price */
            price: number;
            category: components["schemas"]["Category"];
            /** Post */
            post: {
                /** Id */
                id: string;
                /** Collection */
                collection: string;
            } | null;
        };
        /** ValidationError */
        ValidationError: {
            /** Location */
            loc: (string | number)[];
            /** Message */
            msg: string;
            /** Error Type */
            type: string;
        };
    };
    responses: never;
    parameters: never;
    requestBodies: never;
    headers: never;
    pathItems: never;
}
export type SchemaCategory = components['schemas']['Category'];
export type SchemaHttpValidationError = components['schemas']['HTTPValidationError'];
export type SchemaProduct = components['schemas']['Product'];
export type SchemaValidationError = components['schemas']['ValidationError'];
export type $defs = Record<string, never>;
export interface operations {
    root__get: {
        parameters: {
            query?: {
                query?: string;
                sort?: string;
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["Product"][];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
        };
    };
}
