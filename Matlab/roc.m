function [tpf, fpf] = roc( truth, results )

tpf = sum(repmat(truth,1,size(results,2)).*results, 1)./sum(truth);
fpf = sum(repmat(1-truth,1,size(results,2)).*results,1)./sum(1-truth);

[fpf, ix] = sort(fpf);
tpf = tpf(ix);

end

