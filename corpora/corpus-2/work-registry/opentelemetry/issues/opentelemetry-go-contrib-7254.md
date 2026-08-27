**Source ID**: [SRC-ISSUE-02]

# Issue: otelhttp: Cannot record error for spans when producing new semantic convention (open-telemetry/opentelemetry-go-contrib#7254)

**Canonical URL**: https://github.com/open-telemetry/opentelemetry-go-contrib/issues/7254  
**Author**: XSAM  
**Created**: 2025-04-23T02:21:22Z · **Updated**: 2026-01-13T15:23:09Z  
**Collected**: 2026-07-14T14:35:41Z  
**State**: closed (completed)  
**Labels**: bug, area: instrumentation, instrumentation: otelhttp  
**Milestone**: v1.40.0

---

## Description

### Description

`otelhttp` only uses `span.RecordError(err)` when `errType` is not empty

https://github.com/open-telemetry/opentelemetry-go-contrib/blob/b8572491f2d143672581d1c51693c928d376dff8/instrumentation/net/http/otelhttp/transport.go#L132-L140

But `ErrorType` method never returns an empty attribute.

https://github.com/open-telemetry/opentelemetry-go-contrib/blob/b8572491f2d143672581d1c51693c928d376dff8/instrumentation/net/http/httptrace/otelhttptrace/internal/semconv/httpconv.go#L443-L458

### Expected behavior

I don't have a preference on whether we should record `error.type` with `exception.type` at the same time. But the comment and the logic here seem conflicted. 


## Discussion (15)

**dmathieu** — 2025-04-23T08:03:12Z

I don't know what was the intent there. But it feels like `ErroTypeOther` should be the case where we want to fallback to recording an error?

---

**XSAM** — 2025-04-23T16:07:50Z

> But it feels like ErroTypeOther should be the case where we want to fallback to recording an error?

I don't find a way to make it return `ErrorTypeOther`. In most cases, it returns `semconv.ErrorTypeKey.String("*errors.errorString")`.

For instance, errors created by `errors.New()` like `driver.ErrBadConn`. The type is `*errors.errorString`.

I know it is difficult (or impossible) to get this via reflect, but do you think returning `semconv.ErrorTypeKey.String("database/sql/driver.ErrBadConn")` is the ideal result for `driver.ErrBadConn`?

> where we want to fallback to recording an error?

I feel we should always make span recording the error, as this is the only way users can choose to record [`exception.message`](https://github.com/open-telemetry/semantic-conventions/blob/4676c009fa6b8f4ed7d2321c991024373e77428e/docs/attributes-registry/exception.md#exception-message) and [`exception.stacktrace`](https://github.com/open-telemetry/semantic-conventions/blob/4676c009fa6b8f4ed7d2321c991024373e77428e/docs/attributes-registry/exception.md#exception-stacktrace). While only know the error type does not seem to help a lot, these two attributes are very helpful when debugging.

@open-telemetry/go-maintainers What do you think about this issue?

---

**XSAM** — 2025-04-24T18:26:30Z

More information: https://opentelemetry.io/docs/specs/otel/trace/exceptions/ (not in the semconv doc)

The spec about exceptions says

> An exception SHOULD be recorded as an Event on the span during which it occurred if and only if it remains unhandled **when the span ends and causes the span status to be set to ERROR**.

It even has a pseudo code that sets the `error.type` attribute for spans and calls `recordException` at the same time.

```java
Span span = myTracer.startSpan(/*...*/);
try {
  // Code that does the actual work which the Span represents
} catch (Throwable e) {
  span.recordException(e);
  span.setAttribute(AttributeKey.stringKey("error.type"), e.getClass().getCanonicalName())
  span.setStatus(StatusCode.ERROR, e.getMessage());
  throw e;
} finally {
  span.end();
}
```

---

So, a good start for us is to change the code from

```go
		// set error type attribute if the error is part of the predefined
		// error types.
		// otherwise, record it as an exception
		if errType := t.semconv.ErrorType(err); errType.Valid() {
			span.SetAttributes(errType)
		} else {
			span.RecordError(err)
		}

		span.SetStatus(codes.Error, err.Error())
```

to

```go
		// ErrorType should always return a valid error.type` for error
		span.SetAttributes(t.semconv.ErrorType(err))
		span.RecordError(err)
		span.SetStatus(codes.Error, err.Error())
```

---

**pellared** — 2025-06-11T12:24:35Z

What is the value of recording the error as event if the type is set as attribute and value (`err.Error()`) as status description?

> An exception SHOULD be recorded as an Event on the span during which it occurred if and only if it remains unhandled when the span ends and causes the span status to be set to ERROR.

I argue that error result is not an exception. For me a `panic` that was not being recovered is an unhandled exception. We already cover this part of this specification here:

https://github.com/open-telemetry/opentelemetry-go/blob/bc531cb3f9ce9c328b12e473b6409784728dc608/sdk/trace/span.go#L465-L482

Additionally see: https://github.com/open-telemetry/semantic-conventions/blob/main/docs/general/recording-errors.md#recording-errors-on-spans

Therefore, we should not call `span.RecordError(err)`.

---

**dashpole** — 2025-06-12T17:03:33Z

@pellared does that mean span.RecordError should essentially never be called by instrumentation, since panic recovery is already handled by the SDK?

Almost makes it seem like we should deprecate RecordError in the API, and document that End should handle recording exceptions for panics.

---

**pellared** — 2025-06-13T07:21:05Z

My proposal is to not use `span.RecordError` for **terminating errors** per [recording errors on spans semantic conventions](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/general/recording-errors.md#recording-errors-on-spans).

During the SIG meeting, it was also noted that `span.RecordError` captures a stack trace. However, since the stack trace reflects where the error was recorded, not where it originated, I don’t find it particularly valuable. Additionally, capturing and emitting a stack trace has a performance cost. In most languages with exception handling (such as Java or .NET), the stack trace is already included in the thrown exception so the cost of capturing the stack trace was already taken and the stack trace is taken in the place where the exception was thrown.

> @pellared does that mean span.RecordError should essentially never be called by instrumentation, since panic recovery is already handled by the SDK? Almost makes it seem like we should deprecate RecordError in the API,

I believe [`span.RecordError`](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/trace/api.md#record-exception) remains valuable, particularly for **non-terminating errors**. A common use case is **retry logic**, where errors occur but don't immediately end the span. This is especially relevant in the context of **custom instrumentation**, where developers have full control and can explicitly record such intermediate errors.

While instrumentation libraries typically just return errors, they could also benefit from `span.RecordError` if the underlying library provides hooks into retry or failure logic. In such cases, recording retry attempts as span events via `span.RecordError` gives users better visibility into transient issues **without prematurely ending the span**.

For these reasons, I don’t think `span.RecordError` should be deprecated. It might be worth capturing these use cases in the [error recording semantic conventions](https://github.com/open-telemetry/semantic-conventions/blob/main/docs/general/recording-errors.md) (cc @lmolkova).

Side note: There is an OTEP https://github.com/open-telemetry/opentelemetry-specification/pull/4333 that proposes to record exceptions/errors as log records instead of span events.

>  and document that End should handle recording exceptions for panics.

I think that documenting that `span.End` should handle recording exceptions for panics is a good idea.

In my opinion, this is how we implement [recording an exception](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/trace/exceptions.md#recording-an-exception) in the most possible user-friendly way.







---

**pellared** — 2025-06-16T07:44:04Z

I created 

- https://github.com/open-telemetry/opentelemetry-go-contrib/issues/7470
- https://github.com/open-telemetry/opentelemetry-go/issues/6904
- https://github.com/open-telemetry/opentelemetry-go/issues/6903

I think it might be also good to add some "error recording" recommendations in https://pkg.go.dev/go.opentelemetry.io/otel/trace. However, we should first clarify it on the semantic conventions side.

>  I believe [`span.RecordError`](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/trace/api.md#record-exception) remains valuable, particularly for **non-terminating errors**. A common use case is **retry logic**, where errors occur but don't immediately end the span. This is especially relevant in the context of **custom instrumentation**, where developers have full control and can explicitly record such intermediate errors.

This seems not compliant with https://github.com/open-telemetry/semantic-conventions/blob/main/docs/general/recording-errors.md#recording-errors-on-metrics

> Errors that were retried or handled (allowing an operation to complete gracefully) SHOULD NOT be recorded on spans or metrics that describe this operation.

Currently, the only use case I see the only use of `span.RecordError` to use it for "unhandled exceptions" (which for Go can be done in the SDK) and to record multiple errors like here:

https://github.com/open-telemetry/opentelemetry-go-contrib/blob/9e39469c07651d62d1acd5155ddf9843c1b63436/instrumentation/github.com/gin-gonic/gin/otelgin/gin.go#L119-L124

I do not find the semantic conventions clear and probably some work is also needed there.

CC @lmolkova

---

**XSAM** — 2025-08-03T20:45:58Z

Sorry for joining the discussion late.

@pellared I am confused about what we should do to handle errors, especially **non-terminating errors**. Should we do nothing if we encounter an error?

For instance, when facing code like this, do we do nothing for the error we receive?

```go
ctx, span := tracer.Tracer(instrumentationName).Start(ctx, "example")
defer span.End()

err := query(ctx, db)
if err != nil {
	return err
}
return nil
```

Or, should we record this error?

```go
ctx, span := tracer.Tracer(instrumentationName).Start(ctx, "example")
defer span.End()

err := query(ctx, db)
if err != nil {
	span.RecordError(err)
	return err
}
return nil
```

---

I don't think we should just ignore the error without recording it in the span. `RecordError` has `semconv.ExceptionMessage(err.Error())` to record error message, which is always useful when debugging.

Are you trying to limit the usage of `RecordError` to only instrumentation? Why can the instrumentation record the error message?

---

**pellared** — 2025-08-04T15:12:11Z

> For instance, when facing code like this,

It looks like a **terminating** error to me which falls into https://github.com/open-telemetry/semantic-conventions/blob/main/docs/general/recording-errors.md#recording-errors-on-spans:

> When the operation ends with an error, instrumentation:



---

**XSAM** — 2025-08-05T06:38:55Z

I see. So, your proposal is

```go
ctx, span := tracer.Tracer(instrumentationName).Start(ctx, "example")
defer span.End()

err := query(ctx, db)
if err != nil {
	span.SetAttributes(semconv.ErrorType(err))
	span.SetStatus(codes.Error, err.Error())
	return err
}
return nil
```

It makes sense.

---

**pellared** — 2025-08-05T06:40:03Z

Correct 

---

**XSAM** — 2025-08-05T06:50:03Z

> In such cases, recording retry attempts as span events via span.RecordError gives users better visibility into transient issues without prematurely ending the span.

Would it be strange to say we only record `exception` events when `panic` and retriable error happens? Retriable errors do not seem to be categorized as a type of `exception`.

---

**pellared** — 2025-11-03T13:34:57Z

My plan is to add OTel Go specfic "recording errors" guidelines into our [Style Guide](https://github.com/open-telemetry/opentelemetry-go/blob/main/CONTRIBUTING.md#style-guide). Maybe it should be part of some more public user-facing docs like https://pkg.go.dev/go.opentelemetry.io/otel/trace. However, I prefer first trying it out more internally. One of the reasons is that https://github.com/open-telemetry/semantic-conventions/blob/main/docs/general/recording-errors.md#recording-errors-on-spans is "Development" and would need to be "Stable" first. I would work on it on the scope of:
- https://github.com/open-telemetry/opentelemetry-go-contrib/issues/7470

I also think that stabilization of https://github.com/open-telemetry/semantic-conventions/blob/main/docs/general/recording-errors.md#recording-errors-on-spans is a blocker for v1 of `otelhttp`. 

@open-telemetry/go-maintainers, do any thoughts or other proposals?

---

**dashpole** — 2025-11-03T14:55:36Z

Would your proposed guidlines be in-line with the current Development spec, or are you proposing something new?  If they are in-line with that spec, then SGTM.  Otherwise, I would prefer if you updated the spec first so our instrumentation libraries don't get out ahead of the spec.

---

**pellared** — 2025-11-03T15:00:09Z

> Would your proposed guidlines be in-line with the current Development spec, or are you proposing something new?

I want them to be following the current semantic conventions that are in Development

## Timeline

- 2025-04-23T02:21:22Z · **labeled** by XSAM `area: instrumentation`
- 2025-04-23T02:21:22Z · **labeled** by XSAM `bug`
- 2025-04-23T02:21:22Z · **labeled** by XSAM `instrumentation: otelhttp`
- 2025-04-23T02:22:14Z · **renamed** by XSAM "otelhttp: Cannot record error when producing new semantic convention" → "otelhttp: Cannot record error for spans when producing new semantic convention"
- 2025-06-10T14:53:31Z · **cross-referenced** by dmathieu ← https://github.com/open-telemetry/opentelemetry-go-contrib/pull/7456
- 2025-06-16T07:32:18Z · **cross-referenced** by pellared ← https://github.com/open-telemetry/opentelemetry-go-contrib/issues/7470
- 2025-06-16T07:40:13Z · **cross-referenced** by pellared ← https://github.com/open-telemetry/opentelemetry-go/issues/6903
- 2025-09-18T16:17:38Z · **milestoned** by MrAlias → v1.39.0
- 2025-10-16T20:42:15Z · **cross-referenced** by pellared ← https://github.com/open-telemetry/semantic-conventions/pull/2296
- 2025-11-03T09:39:05Z · **cross-referenced** by pellared ← https://github.com/open-telemetry/opentelemetry-go/issues/6648
- 2025-11-03T14:23:56Z · **cross-referenced** by dmathieu ← https://github.com/open-telemetry/opentelemetry-go-contrib/issues/8107
- 2025-12-04T18:17:39Z · **demilestoned** by MrAlias → v1.39.0
- 2025-12-04T18:17:39Z · **milestoned** by MrAlias → v1.40.0
- 2025-12-19T13:23:07Z · **cross-referenced** by pellared ← https://github.com/open-telemetry/semantic-conventions/pull/3228
- 2026-01-12T17:33:42Z · **cross-referenced** by pellared ← https://github.com/open-telemetry/opentelemetry-go-contrib/pull/8386
- 2026-01-13T15:23:09Z · **closed** by pellared
- 2026-04-27T06:41:51Z · **cross-referenced** by coderabbitai[bot] ← https://github.com/centos-automotive-suite/automotive-dev-operator/pull/260
- 2026-06-04T00:54:06Z · **cross-referenced** by coderabbitai[bot] ← https://github.com/redhat-et/docsclaw/pull/89

